from django.views.generic import TemplateView


class HomeTemplateView(TemplateView):
    """ Главная страница. """

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """ Передача названия текущей страницы в шаблон. """

        context = super().get_context_data(**kwargs)
        context["current_page"] = "Главная"

        return context
