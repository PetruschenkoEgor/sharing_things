from django import forms
from .models import Ad


class AdForm(forms.ModelForm):
    """ Форма для объявления. """
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets = {
            'condition': forms.Select(attrs={'class': 'form-control'}),
        }
