from django.urls import path, include
from .views import OffersListView, OffersDetailView, DetailsView

urlpatterns = [
    path('offers/', OffersListView.as_view(), name='offerdetail-detail'),
    path('offers/<int:pk>/', OffersDetailView.as_view(), name='offers-detail'),
    path('offerdetails/<int:pk>/', DetailsView.as_view(), name='offerdetails-detail'),
]