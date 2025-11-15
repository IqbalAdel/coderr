from django.urls import path, include
from .views import ReviewViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    # path('order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    # path('completed-order-count/<int:pk>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
]