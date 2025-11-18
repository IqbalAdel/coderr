from rest_framework import generics, status
from .serializers import ProfileDetailSerializer, ProfileBusinessSerializer, ProfileCustomerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Profile
from .permissions import ProfileEditPermission

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for profiles of specific users.

    Returns the user data of specific primary key.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated, ProfileEditPermission]

class ProfileBusinessListView(generics.ListAPIView):
    """
    API endpoint for view of Business Profiles .

    Lists Business Profiles where the user is authenticated user
    """
    serializer_class = ProfileBusinessSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Profile.objects.all()
        queryset = queryset.filter(type='business')
        return queryset

class ProfileCustomerListView(generics.ListAPIView):
    """
    API endpoint for view of Customer Profiles .

    Lists Customer Profiles where the user is authenticated user
    """
    serializer_class = ProfileCustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Profile.objects.all()
        queryset = queryset.filter(type='customer')
        return queryset