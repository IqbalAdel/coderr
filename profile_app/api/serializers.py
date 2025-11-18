from rest_framework import serializers, status
from rest_framework.response import Response
from ..models import Profile
from django.contrib.auth import get_user_model

class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile objects.
    Handles validation and serialization of Profile data.
    """
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']

    def validate_username(self, value):
        user = self.instance  
        if get_user_model().objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

class ProfileBusinessSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile objects.
    Handles validation and serialization of Profile data with the business type.
    """
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 'tel', 'description', 'working_hours', 'type']

class ProfileCustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile objects.
    Handles validation and serialization of Profile data with the customer type.
    """
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'type']