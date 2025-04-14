from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

from ads.forms import AdForm
from ads.models import Ad


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
    success_url = reverse_lazy('ads:home')

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
