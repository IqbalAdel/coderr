from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from ..models import Profile
from ..api.serializers import ProfileBusinessSerializer, ProfileCustomerSerializer


class GetProfileListsTests(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='exampleUsername',
            password='examplePassword',
            email='web@dev.com',
            type='business'
            )
        self.user2 = get_user_model().objects.create_user(
            username='exampleUsername2',
            password='examplePassword2',
            email='web2@dev.com',
            type='customer'
            )
        self.user3 = get_user_model().objects.create_user(
            username='exampleUsername3',
            password='examplePassword3',
            email='web3@dev.com',
            type='customer'
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
        
        self.profile2 = Profile.objects.create(
            user=self.user2, 
            username=self.user2.username, 
            first_name= '',
            last_name= '',
            file='',
            location='',
            tel='',
            description='',
            working_hours = '',
            type=self.user2.type,
            email=self.user2.email,
            created_at="2023-01-01T12:00:00Z"
            )
        
        self.profile3 = Profile.objects.create(
            user=self.user3, 
            username=self.user3.username, 
            type=self.user3.type,
            email=self.user3.email,
            created_at="2023-01-01T12:00:00Z"
            )

    def test_get_profiles_business_OK(self):
        url = reverse('business-list')
        response = self.client.get(url)
        expected_data = ProfileBusinessSerializer(
            Profile.objects.filter(type='business'), many=True
        ).data
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_profiles_customer_OK(self):
        url = reverse('customer-list')
        response = self.client.get(url)
        expected_data = ProfileCustomerSerializer(
            Profile.objects.filter(type='customer'), many=True
        ).data
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_business_list_UNAUTHORIZED(self):
        url = reverse('business-list') 
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_customer_list_UNAUTHORIZED(self):
        url = reverse('customer-list') 
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
