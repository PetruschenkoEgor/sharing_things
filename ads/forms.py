from django import forms

from .mixins import StyleFormMixin
from .models import Ad


class AdForm(StyleFormMixin, forms.ModelForm):
    """ Форма для объявления. """
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        # widgets = {
        #     'condition': forms.Select(attrs={'class': 'form-control'}),
        # }
