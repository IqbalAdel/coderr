from rest_framework import viewsets, generics, permissions, status
from .serializers import OfferListSerializer,OfferCreateSerializer, OffersDetailSerializer, OfferUpdateSerializer, DetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Offer, OfferDetail
from .permissions import OfferPermissions
from .paginations import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from django.db.models import Min

class OfferFilter(filters.FilterSet):
    """
    Custom-Filter for offer-list objects, optional for the creator_id, min_price and max_delivery_time 
    """
    creator_id = filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    min_price = filters.NumberFilter(method='filter_min_price')
    max_delivery_time = filters.NumberFilter(method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id']

    def filter_min_price(self, queryset, name, value):
        """Filter offers where any detail has a price >= given value."""
        return queryset.filter(details__price__gte=value).distinct()

    def filter_max_delivery_time(self, queryset, name, value):
        """Filter offers where any detail has delivery time <= given value."""
        return queryset.filter(details__delivery_time_in_days__lte=value).distinct()

class OffersListView(generics.ListCreateAPIView):
    """
    API endpoint for listing Offers.

    Lists all Offers made by Business users. Includes Custom Pagination, Search, Ordering and Filter.
    """
    queryset = Offer.objects.all()
    permission_classes = [OfferPermissions]
    filterset_class = OfferFilter
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at', 'min_price']


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OfferListSerializer     
        return OfferCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = (
            Offer.objects
            .annotate(min_price=Min('details__price'))  
        )
        return queryset

class OffersDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for view of specific Offers.

    Lists specific Offers where the user is authenticated user,
    and allows updating, deleting an offer where the requesting user is set as the business user who made the offer.
    """
    queryset = Offer.objects.all()
    permission_classes = [OfferPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OffersDetailSerializer      
        return OfferUpdateSerializer

class DetailsView(generics.RetrieveAPIView):
    """
    API endpoint for view of specific Offer-Details.

    Lists specific Offer-Details where the user is authenticated user.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = DetailSerializer
    permission_classes = [IsAuthenticated]