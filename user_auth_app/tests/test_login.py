from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
# from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from user_auth_app.api.serializers import RegistrationSerializer, LoginAuthTokenSerializer


class LoginTests(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='exampleUsername',
            password='examplePassword',
            )

    def test_login_user_happy(self):
        url = reverse('login')
        data = {'username':'exampleUsername',
                'password': 'examplePassword',
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_response_data(self):
        url = reverse('login')
        data = {'username':'exampleUsername',
                'password': 'examplePassword',
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
        self.assertIsInstance(response.data, dict)

    # def test_login_content(self):
    #     url = reverse('login')
    #     data = {'username':'exampleUsername',
    #             'password': 'examplePassword',
    #             }
    #     response = self.client.post(url, data, format="json")
    #     expected_data = LoginAuthTokenSerializer(data)
    #     print(response.data)
    #     # print(expected_data.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual({response.data['username'], response.data['password']}, expected_data)

    
    def test_login_wrong_pw_400(self):
        url = reverse('login')
        data = {'username':'exampleUsername',
                'password': 'exPassword',
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_useranme_400(self):
        url = reverse('login')
        data = {'username':'exUsername',
                'password': 'examplePassword',
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_pw_400(self):
        url = reverse('login')
        data = {'username':'exampleUsername',
                'password': '',
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_useranme_400(self):
        url = reverse('login')
        data = {'username':'',
                'password': 'examplePassword',
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_missing_field_useranme_400(self):
        url = reverse('login')
        data = {
                'password': 'examplePassword',
                }
        response = self.client.post(url, data, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def test_register_wrong_email_400(self):
    #     url = reverse('registration')
    #     data = {'username':'exampleUsername',
    #             'email': 'examplemail.de',
    #             'password': 'examplePassword',
    #             'repeated_password':'examplePassword',
    #             'type': 'business'
    #             }
    #     response = self.client.post(url, data, format="json")
    #     # print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
   
   
