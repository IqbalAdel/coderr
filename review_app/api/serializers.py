from rest_framework import serializers
from ..models import Review
from django.contrib.auth import get_user_model

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review objects.
    Handles validation and serialization of Review data.
    """

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )
    reviewer = serializers.PrimaryKeyRelatedField(
        read_only=True
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

    def validate(self, attrs):
        reviewer = self.context['request'].user
        business_user = attrs.get('business_user')

        if Review.objects.filter(reviewer=reviewer, business_user=business_user).exists():
            raise serializers.ValidationError(
                "You have already reviewed this user."
            )
        return attrs