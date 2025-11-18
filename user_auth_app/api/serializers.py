from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from profile_app.models import Profile

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    Handles validation, creation, and serialization of User data.

    Fields:
        id (int): Read-only. Unique identifier of the user.
        username (str): username of the user.
        email (str): Email address of the user. Must be unique.
        password (str): User's password. Write-only.
        repeated_password (str): Confirmation of the password. Write-only; must match `password`.
    """
    repeated_password = serializers.CharField(write_only = True)
    type = serializers.ChoiceField(choices=[('customer', 'Customer'), ('business', 'Business')])

    class Meta:
        model = get_user_model()
        fields = ['id','username','email','password', 'repeated_password', 'type']
        extra_kwargs = {
            'password' : {
                'write_only': True
            },
        }
    
    def validate_username(self, value):       
        value = value.strip()
        if not value:
            res = serializers.ValidationError({'detail': 'Username cannot be empty.'}) 
            res.status_code = 400
            raise res
        saved_name = get_user_model().objects.filter(username=value)
        if value == saved_name:
            res = serializers.ValidationError({'detail': 'Username already exists'}) 
            res.status_code = 400
            raise res
        
        return value

    def validate_email(self, value):         
        if get_user_model().objects.filter(email=value).exists():
            res = serializers.ValidationError('Email already exists') 
            res.status_code = 400
            raise res
        return value
    
    def validate_type(self, value):       
        value = value.strip()
        if not value:
            res = serializers.ValidationError({'detail': 'Type cannot be empty.'}) 
            res.status_code = 400
            raise res
        if value not in ['customer', 'business']:
            res = serializers.ValidationError({'detail': 'Type must be either customer or business.'}) 
            res.status_code = 400
            raise res
        return value

    def save(self):     
        print(self.validated_data)
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        username = self.validated_data['username']
        email = self.validated_data['email']
        type = self.validated_data['type']

        if not email:
            res = serializers.ValidationError({'detail': 'Email cannot be empty.'}) 
            raise res
        
        if not type:
            res = serializers.ValidationError({'detail': 'Type cannot be empty.'}) 
            raise res

        if pw != repeated_pw:
            raise serializers.ValidationError({'detail': 'passwords dont match'}) 
        
        if get_user_model().objects.filter(username=username).exists():
            serializers.ValidationError({'detail': 'Username already exists'}) 
        
        account = get_user_model()(email = self.validated_data['email'], username=username, type=type)
        account.set_password(pw)
        account.save()
        profile = Profile.objects.create(user=account, username=username, email=email, type=type)
        return account
    
class LoginAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for loggin in users.
    Handles validation and serialization of User data.

    Fields:
        username (str): username of the user. Must be unique.
        password (str): User's password. Write-only.
    """

    username = serializers.CharField()
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):    
        password = attrs.get('password')
        username= attrs.get('username')

        user = authenticate(username=username, password=password)
        if not user:
            res = serializers.ValidationError({'detail': 'Invalid username or password.'}) 
            res.status_code = 400
            raise res     
        attrs['user'] = user
        return attrs