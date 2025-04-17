from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    """Регистрация пользователя"""

    model = User
    form_class = UserRegisterForm
    template_name = "user_form.html"
    success_url = reverse_lazy("users:login")


class UserUpdateView(UpdateView):
    """Редактирование пользователя."""

    model = User
    form_class = UserRegisterForm
    template_name = "user_form.html"
    success_url = reverse_lazy("users:personal-account")


class PersonalAccountDetailView(DetailView):
    """Личный кабинет."""

    model = User
    template_name = "personal_account.html"
    context_object_name = "user"
