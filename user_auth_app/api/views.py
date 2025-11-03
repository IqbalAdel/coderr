from rest_framework import generics, status
from .serializers import RegistrationSerializer, LoginAuthTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token 
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        if get_user_model().objects.filter(username=request.data.get('username')).exists():
            return Response(
                {"detail": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST
    )

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user = saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors        
            return Response({'detail': data}, status=status.HTTP_400_BAD_REQUEST) 

class CustomLoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = LoginAuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user = user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:   
            data = serializer.errors
            return Response({'detail':data}, status=status.HTTP_400_BAD_REQUEST)