from django.urls import path

from ads.apps import AdsConfig
from ads.views import HomeTemplateView

app_name = AdsConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
]
