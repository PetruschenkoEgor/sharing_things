from django.contrib.auth.forms import UserCreationForm

from ads.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta:
        model = User
        fields = ("email", "phone", "password1", "password2")

    def __init__(self, *args, **kwargs):
        """Переопределение меток полей."""

        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Пароль"
        self.fields["password2"].label = "Повторите пароль"

        # Отключение help_text для всех полей.
        for field in self.fields.values():
            field.help_text = None
