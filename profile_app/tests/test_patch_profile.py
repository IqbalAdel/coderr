from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from ..models import Profile
from ..api.serializers import ProfileDetailSerializer

class PatchSingleProfileTests(APITestCase):
    
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
            first_name= 'Daria',
            last_name= 'Weile',
            file='profile_picture.jpg',
            location='Frankfurt',
            tel='123456890',
            description='Business description',
            working_hours = '9-17',
            type=self.user2.type,
            email=self.user2.email,
            created_at="2023-01-01T12:00:00Z"
            )
    

    def test_update_profile_unauthenticated_401(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        data = {'first_name': 'Bohn'}
        self.client.logout()
        response = self.client.patch(url, data, format='json')
        self.profile.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.profile.first_name, 'Max')

    def test_update_no_permission_403(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile2.id})
        data = {'first_name': 'Dohn'}
        response = self.client.patch(url, data, format='json')
        self.profile.refresh_from_db()
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.profile.first_name, 'Max')

    
    def test_update_profile_empty_fields(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        data = {'first_name': ''}
        response = self.client.patch(url, data, format='json')
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.first_name, '')

    def test_update_profile_user_model_fields(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        data = {'username': 'Devon', 'email': 'newemail@dev.com'}
        response = self.client.patch(url, data, format='json')
        self.profile.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.username, 'Devon')
        self.assertEqual(self.profile.email, 'newemail@dev.com')
        self.assertEqual(self.user.username, 'Devon')
        self.assertEqual(self.user.email, 'newemail@dev.com')
    
    def test_update_profile_user_model_type(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        data = {'type': ''}
        response = self.client.patch(url, data, format='json')
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.profile.type, 'business')
        self.assertEqual(self.user.type, 'business')

    def test_update_profile_unnullable_fields(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        data = {
            'first_name': None,
            'last_name': None,
            'location': None,
            'tel': None,
            'description': None,
            'working_hours': None,
            'type': None,
        }
        response = self.client.patch(url, data, format='json')
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.profile.first_name, None)
        self.assertNotEqual(self.profile.last_name, None)
        self.assertNotEqual(self.profile.location, None)
        self.assertNotEqual(self.profile.tel, None)
        self.assertNotEqual(self.profile.description, None)
        self.assertNotEqual(self.profile.working_hours, None)
        

    def test_update_profile_not_found_404(self):
        url = reverse('profile-detail', kwargs={'pk': 100})
        data = {'first_name': 'Cohn'}
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_profile_first_name(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        data = {'first_name': 'John'}
        response = self.client.patch(url, data, format='json')
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.first_name, 'John')

    def test_update_profile_content(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        data = {'first_name': 'Mon'}
        response = self.client.patch(url, data, format='json')
        self.profile.refresh_from_db()
        expected_data = ProfileDetailSerializer(self.profile).data

        self.assertEqual(response.data, expected_data)
        self.assertNotIn('password', response.data)
        self.assertNotIn('repeated_password', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile_empty_username_email(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.id})
        data = {'username': '', 'email': ''}
        response = self.client.patch(url, data, format='json')
        self.profile.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.profile.username, '')
        self.assertNotEqual(self.profile.email, '')