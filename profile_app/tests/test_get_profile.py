from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from ..models import Profile
from ..api.serializers import ProfileDetailSerializer


class GetSingleProfileTests(APITestCase):
    
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
        self.user4 = get_user_model().objects.create_user(
            username='exampleUsername4',
            password='examplePassword4',
            email='web4@dev.com',
            type='customer'
            )
        self.user5 = get_user_model().objects.create_user(
            username='exampleUsername5',
            password='examplePassword5',
            email='web5@dev.com',
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

    def test_time_profile(self):
        self.assertEqual(
           self.profile3.created_at.isoformat().replace('+00:00', 'Z'),
           '2023-01-01T12:00:00Z'
        )
  

    def test_missing_required_field_raises_error(self):
        profile4 = Profile(
                user=self.user4, 
                username=self.user4.username, 
                first_name=None,
                last_name=None,  
                location=None,
                tel=None,
                description=None,
                working_hours=None,
                type=self.user4.type,
                email=self.user4.email,
            )
        self.assertIsNone(profile4.first_name)
        self.assertIsNone(profile4.last_name)
        self.assertIsNone(profile4.location)
        self.assertIsNone(profile4.tel)
        self.assertIsNone(profile4.description)
        self.assertIsNone(profile4.working_hours)

    def test_get_profile_OK(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile2_BLANK_OK(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile3_MISSINGwithDEFAULT_200(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile3.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_profile_correct_content(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id}) 
        response = self.client.get(url)
        expected_data = ProfileDetailSerializer(self.profile).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_profile_UNAUTHORIZED(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id}) 
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_NOTFOUND(self):
        url = reverse('profile-detail', kwargs={'pk': 404}) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)