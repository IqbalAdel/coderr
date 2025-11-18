from rest_framework import viewsets, generics, permissions, status
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import OrderPermissions
from ..models import Order
from rest_framework import mixins, viewsets

class CreateListUpdateDestroyViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    Custom ViewsetClass for further use.
    """
    pass

class OrderViewSet(CreateListUpdateDestroyViewSet):
    """
    API endpoint for view of Orders.

    Lists Orders where the user is authenticated user,
    and allows updating, deleting, creating an order where the requesting user is set as the customer user who made the order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [OrderPermissions]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(customer_user=user) | Order.objects.filter(business_user=user)
        return Order.objects.none()

class OrderCountView(generics.RetrieveAPIView):
    """
    API endpoint for view of Order statistic. Shows Order count placed for a specific business user
    """
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        order_count = Order.objects.filter(business_user__id=pk).count()
        return Response({'order_count': order_count}, status=status.HTTP_200_OK)
    
class CompletedOrderCountView(generics.RetrieveAPIView):
    """
    API endpoint for view of Order statistic. Shows Order count placed for a specific business user, which were completed
    """
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        completed_order_count = Order.objects.filter(business_user__id=pk, status='completed').count()
        return Response({'completed_order_count': completed_order_count}, status=status.HTTP_200_OK)