from django.urls import path

from ads.apps import AdsConfig
from ads.views import HomeTemplateView, AdCreateView, AdListView, AdDetailView, AdMyListView, AdUpdateView, \
    AdDeleteView, ExchangeProposalCreate, ExchangeProposalListView, MyExchangeProposalListView, \
    OffersExchangeProposalListView, AcceptExchangeProposalView, RefuseExchangeProposalView, ExchangeProposalDeleteView, \
    AdSearchListView

app_name = AdsConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('ad-create/', AdCreateView.as_view(), name='ad-create'),
    path('ads/', AdListView.as_view(), name='ads-list'),
    path('my_ads/', AdMyListView.as_view(), name='ads-mylist'),
    path('<int:pk>/ad/', AdDetailView.as_view(), name='ad-detail'),
    path('<int:pk>/update/', AdUpdateView.as_view(), name='ad-update'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),
    path('exchange-create/<int:pk>/', ExchangeProposalCreate.as_view(), name='exchange-create'),
    path('exchanges/', ExchangeProposalListView.as_view(), name='exchanges-list'),
    path('my_exchanges/', MyExchangeProposalListView.as_view(), name='my-exchanges-list'),
    path('offers_exchanges/', OffersExchangeProposalListView.as_view(), name='offers-exchanges'),
    path('accept-exchange-proposal/<int:pk>/', AcceptExchangeProposalView.as_view(), name='accept-exchange-proposal'),
    path('refuse-exchange-proposal/<int:pk>/', RefuseExchangeProposalView.as_view(), name='refuse-exchange-proposal'),
    path('delete-exchange-proposal/<int:pk>/', ExchangeProposalDeleteView.as_view(), name='delete-exchange-proposal'),
    path('search/', AdSearchListView.as_view(), name='search-ads'),
]
