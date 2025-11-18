from rest_framework import viewsets, generics, permissions, status
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import ReviewPermissions
from ..models import Review
from rest_framework import mixins, viewsets

class CreateListUpdateDestroyViewSet(
                                mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.DestroyModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    Custom ViewsetClass for further use.
    """
    pass

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint for view of Reviews.

    Lists Reviews where the user is authenticated user,
    and allows updating, creating, deleting a review where the requesting user is set as the reviewer who made the review.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermissions]

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)