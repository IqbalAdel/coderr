from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from user_auth_app.api.serializers import RegistrationSerializer


class RegistrationTests(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='exampleUsername',
            password='examplePassword',
            )
    def test_user_creation(self):
        self.assertEqual(self.user.username, 'exampleUsername')
        self.assertEqual(self.user.check_password('examplePassword'), True)
        # self.client = APIClient()
        # self.client.login(username='testuser', password='testpassword')

        # self.client = APIClient()
        # self.token = Token.objects.create(user = self.user)
        # self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)

    def test_register_include_data(self):
        url = reverse('registration')
        data = {'username':'newUsername',
                'email': 'new@mail.de',
                'password': 'examplePassword',
                'repeated_password':'examplePassword',
                'type': 'business'
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertIn('token', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('user_id', response.data)    
        self.assertNotIn('password', response.data)
        self.assertNotIn('repeated_password', response.data)
        self.assertNotIn('type', response.data)

    def test_register_user_happy(self):
        url = reverse('registration')
        data = {'username':'newUsername',
                'email': 'new@mail.de',
                'password': 'examplePassword',
                'repeated_password':'examplePassword',
                'type': 'business'
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_register_wrong_pw_400(self):
        url = reverse('registration')
        data = {'username':'exampleUsername',
                'email': 'example@mail.de',
                'password': 'examplePassword',
                'repeated_password':'examplPassword',
                'type': 'business'
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_wrong_email_400(self):
        url = reverse('registration')
        data = {'username':'exampleUsername',
                'email': 'examplemail.de',
                'password': 'examplePassword',
                'repeated_password':'examplePassword',
                'type': 'business'
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_response_user_registration(self):
    #     url = reverse('registration')
    #     data = {'username':'testuser',
    #             'email': 'web@dev.com',
    #             'password': 'testpassword',
    #             'repeated_password':'testpassword',
    #             'type': 'customer'
    #             }
    #     response = self.client.post(url, data, format="json")
    #     expected_data = RegistrationSerializer(self.user).data

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(response.data, expected_data)
   
   
