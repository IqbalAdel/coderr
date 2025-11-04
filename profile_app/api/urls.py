from django.urls import path
from .views import ProfileDetailView, ProfileBusinessListView, ProfileCustomerListView 

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/business/', ProfileBusinessListView.as_view(), name='business-list'),
    path('profiles/customer/', ProfileCustomerListView.as_view(), name='customer-list'),
]