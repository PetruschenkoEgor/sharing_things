from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from ads.forms import AdForm, ExchangeProposalForm
from ads.models import Ad, ExchangeProposal


class HomeTemplateView(TemplateView):
    """ Главная страница. """

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context["current_page"] = "Главная"

        return context


class AdCreateView(CreateView):
    """ Создание объявления. """

    model = Ad
    form_class = AdForm
    template_name = 'ad_form.html'
    success_url = reverse_lazy('ads:ads-mylist')

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context['current_page'] = 'Добавление обявления'

        return context

    def form_valid(self, form):
        """ Добавляет текущего пользователя, как создателя объявления. """

        ad = form.save(commit=False)
        ad.user = self.request.user
        ad.save()

        return super().form_valid(form)


class AdListView(ListView):
    """ Список объявлений. """

    model = Ad
    template_name = 'ads.html'
    context_object_name = 'ads'

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context['current_page'] = 'Объявления'

        return context

    def get_queryset(self):
        """ Возвращает объявления других пользователей. """

        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.exclude(user=user)

        return queryset


class AdMyListView(ListView):
    """ Список моих объявлений. """

    model = Ad
    template_name = 'ads.html'
    context_object_name = 'ads'

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context['current_page'] = 'Мои объявления'

        return context

    def get_queryset(self):
        """ Возвращает объявления текущего пользователя. """

        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(user=user)
        else:
            queryset = Ad.objects.none()

        return queryset


class AdDetailView(DetailView):
    """ Информация об объявлении. """

    model = Ad
    template_name = 'ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context['current_page'] = 'Объявление'

        return context


class AdUpdateView(UpdateView):
    """ Редактирование объявления. """

    model = Ad
    form_class = AdForm
    template_name = 'ad_form.html'
    success_url = reverse_lazy('ads:ads-mylist')

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context['current_page'] = 'Редактирование'

        return context


class AdDeleteView(DeleteView):
    """ Удаление объявления. """

    model = Ad
    template_name = 'confirm-delete.html'
    success_url = reverse_lazy('ads:ads-mylist')

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context['current_page'] = 'Удаление объявления'

        return context


class ExchangeProposalCreate(CreateView):
    """ Создание обмена. """

    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = 'exchange_proposal_form.html'
    success_url = reverse_lazy('ads:ads-list')

    def get_form_kwargs(self):
        """ Передаем текущего пользователя в форму. """

        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})

        return kwargs

    def form_valid(self, form):
        """ Автоматически устанавливаем объявление отправителя и делаем владельцем текущего пользователя. """

        user = self.request.user
        ad_id = self.kwargs.get('pk')
        sender_ad = Ad.objects.get(id=ad_id)
        form.instance.ad_sender = sender_ad
        form.instance.owner = user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        ad_id = self.kwargs.get('pk')
        context['current_page'] = 'Предложение обмена'
        context['ad'] = Ad.objects.get(id=ad_id)

        return context


class ExchangeProposalListView(ListView):
    """ Список обменов. """

    model = ExchangeProposal
    template_name = 'exchange_proposals.html'
    context_object_name = 'exchanges_ok'

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон и списков состоявшихся и не состоявшихся обменов. """

        context = super().get_context_data(**kwargs)
        user = self.request.user
        users_ads = Ad.objects.filter(user=user)
        context['current_page'] = 'Обмены'
        # принятые обмены
        context['exchanges_ok'] = ExchangeProposal.objects.filter(Q(ad_sender__in=users_ads) | Q(ad_receiver__in=users_ads), status='Подтвержден')
        # отклоненные обмены
        context['exchanges'] = ExchangeProposal.objects.filter(Q(ad_sender__in=users_ads) | Q(ad_receiver__in=users_ads), status='Отклонен')

        return context


class MyExchangeProposalListView(ListView):
    """ Я предлагаю поменяться. """

    model = ExchangeProposal
    template_name = 'exchange_proposals1.html'
    context_object_name = 'exchanges'

    def get_queryset(self):
        """ Возвращает предложения обмена созданные текущим пользователем. """

        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.filter(owner=user, status='Ожидает')
        else:
            queryset = Ad.objects.none()

        return queryset

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context['current_page'] = 'Вы предлагаете обмен'

        return context


class OffersExchangeProposalListView(ListView):
    """ Вам предлагают поменяться. """

    model = ExchangeProposal
    template_name = 'exchange_proposals1.html'
    context_object_name = 'exchanges'

    def get_queryset(self):
        """ Возвращает предложения обмена от других пользователей. """

        queryset = super().get_queryset()
        user = self.request.user
        users_ads = Ad.objects.filter(user=user)
        queryset = ExchangeProposal.objects.filter(ad_sender__in=users_ads, status='Ожидает')

        return queryset

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context['current_page'] = 'Вам предлагают обмен'

        return context


class AcceptExchangeProposalView(SingleObjectMixin, View):
    """ Обрабатывает нажатие кнопки Принять предложение(принять обмен). """

    model = ExchangeProposal

    def post(self, request, *args, **kwargs):
        proposal = self.get_object()
        proposal.status = 'Подтвержден'
        proposal.save()

        return HttpResponseRedirect(reverse('ads:offers-exchanges'))


class RefuseExchangeProposalView(SingleObjectMixin, View):
    """ Обрабатывает нажатие кнопки Отказаться(отказаться от обмена). """

    model = ExchangeProposal

    def post(self, request, *args, **kwargs):
        proposal = self.get_object()
        proposal.status = 'Отклонен'
        proposal.save()

        return HttpResponseRedirect(reverse('ads:offers-exchanges'))


class ExchangeProposalDeleteView(DeleteView):
    """ Удаление предложения об обмене. """

    model = ExchangeProposal
    success_url = reverse_lazy('ads:my-exchanges-list')
