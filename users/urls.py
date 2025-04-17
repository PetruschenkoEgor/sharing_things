from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import PersonalAccountDetailView, UserCreateView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path("user/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("personal-account/<int:pk>/", PersonalAccountDetailView.as_view(), name="personal-account"),
]
