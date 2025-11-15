from rest_framework import serializers
from ..models import Review


class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        read_only=True, source='business_user'
    )
    reviewer = serializers.PrimaryKeyRelatedField(
        read_only=True, source='reviewer'
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 
                  'business_user',
                  'reviewer',
                  'rating',
                  'description',
                  'created_at', 
                  'updated_at']