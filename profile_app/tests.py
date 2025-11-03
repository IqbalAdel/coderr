from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import Profile
# from user_auth_app.api.serializers import RegistrationSerializer, LoginAuthTokenSerializer


class ProfileTests(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='exampleUsername',
            password='examplePassword',
            email='web@dev.com',
            type='business'
            )
        self.client = APIClient()
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        self.profile = Profile.objects.create(
            user=self.user, 
            username=self.user.username, 
            first_name= 'Max',
            last_name= 'Mustermann',
            file='profile_picture.jpg',
            location='Frankfurt',
            tel='123456890',
            description='Business description',
            working_hours = '9-17',
            type=self.user.type,
            email=self.user.email,
            created_at="2023-01-01T12:00:00Z"
            )

    def test_profile_creation(self):
        self.assertEqual(self.profile.id, self.user.id)
        self.assertEqual(self.profile.username, 'exampleUsername')
        self.assertEqual(self.profile.first_name, 'Max')
        self.assertEqual(self.profile.last_name, 'Mustermann')
        self.assertEqual(self.profile.file, 'profile_picture.jpg')
        self.assertEqual(self.profile.location, 'Frankfurt')
        self.assertEqual(self.profile.tel, '123456890')
        self.assertEqual(self.profile.description, 'Business description')
        self.assertEqual(self.profile.working_hours, '9-17')
        self.assertEqual(self.profile.type, 'business')
        self.assertEqual(self.profile.email, 'web@dev.com')
        self.assertEqual(str(self.profile.created_at), "2023-01-01T12:00:00Z")

    # def test_get_profile_detail(self):
    #     url = reverse('profile-detail', kwargs={'pk': self.profile.id}) # für den Get-Befehl
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_profile_detail_content(self):
    #     url = reverse('profile-detail', kwargs={'pk': self.profile.id}) # für den Get-Befehl
    #     response = self.client.get(url)
    #     expected_data = ProfileSerializer(self.profile).data

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data, expected_data)


