from django import forms

from .mixins import StyleFormMixin
from .models import Ad, ExchangeProposal


class AdForm(StyleFormMixin, forms.ModelForm):
    """Форма для объявления."""

    class Meta:
        model = Ad
        fields = ["title", "description", "image_url", "category", "condition"]
        # widgets = {
        #     'condition': forms.Select(attrs={'class': 'form-control'}),
        # }


class ExchangeProposalForm(StyleFormMixin, forms.ModelForm):
    """Форма для обмена."""

    class Meta:
        model = ExchangeProposal
        fields = [
            "ad_receiver",
            "comment",
        ]

    def __init__(self, *args, **kwargs):

        # Устанавливаем queryset, чтобы выбрать только объявления текущего пользователя
        user = kwargs.pop("user", None)  # Получаем пользователя из kwargs и удаляем его оттуда
        super().__init__(*args, **kwargs)

        if user:
            self.fields["ad_receiver"].queryset = Ad.objects.filter(user=user)
        else:
            self.fields["ad_receiver"].queryset = Ad.objects.none()
        self.fields["comment"].initial = ""
