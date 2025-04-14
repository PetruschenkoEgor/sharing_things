from django.urls import path

from ads.apps import AdsConfig
from ads.views import HomeTemplateView, AdCreateView, AdListView, AdDetailView, AdMyListView, AdUpdateView, AdDeleteView

app_name = AdsConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('ad-create/', AdCreateView.as_view(), name='ad-create'),
    path('ads/', AdListView.as_view(), name='ads-list'),
    path('my_ads/', AdMyListView.as_view(), name='ads-mylist'),
    path('<int:pk>/ad/', AdDetailView.as_view(), name='ad-detail'),
    path('<int:pk>/update/', AdUpdateView.as_view(), name='ad-update'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),
]
