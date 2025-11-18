from rest_framework import viewsets, generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from offer_app.models import Offer
from review_app.models import Review
from profile_app.models import Profile
from rest_framework import mixins, viewsets
from django.db.models import Avg

class StatsView(generics.ListAPIView):
    """
    API endpoint for listing specific aggregate statistics.

    -review_count = Sum of all Reviews that were placed for business users by customers.
    -average_rating = Average of all total ratings placed for their reviews
    -profile_count = Sum of all profiles with the business type
    -offer_count = Sum of all existing Offers
    """
    def get(self, request, *args, **kwargs):
        review_count = Review.objects.all().count()
        average_rating = Review.objects.aggregate(avg_rating=Avg("rating"))["avg_rating"]
        profile_count = Profile.objects.filter(type='business').count()
        offer_count = Offer.objects.all().count()

        return Response({
                "review_count": review_count,
                "average_rating": average_rating,
                "business_profile_count": profile_count,
                "offer_count": offer_count
            }, status=status.HTTP_200_OK)