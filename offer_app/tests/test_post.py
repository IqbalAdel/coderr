from rest_framework.test import APITestCase, APIClient, APIRequestFactory, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from ..models import Offer, OfferDetail
from ..api.serializers import OfferListSerializer
from profile_app.models import Profile

class PostOfferTests(APITestCase):
    
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
            type='business'
            )
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
            first_name= 'Maxi',
            last_name= 'Mustermoney',
            file='profile_picture.jpg',
            location='Frankfurt',
            tel='123456890',
            description='Business description',
            working_hours = '9-17',
            type=self.user2.type,
            email=self.user2.email,
            )

        self.client = APIClient()
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        
    def test_post_offer_201(self):
        url = reverse('offerdetail-detail')
        data = {
        "title": "Grafikdesign-Paket",
        "image": None,
        "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        "details": [
            {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "basic"
            },
            {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
            },
            {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
            }
        ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_UNAUTH_401(self):
        url = reverse('offerdetail-detail')
        data = {
        "title": "Grafikdesign-Paket",
        "image": None,
        "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        "details": [
            {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "basic"
            },
            {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
            },
            {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
            }
        ]
        }
        self.client.logout()
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_NOT_BUSINESS_403(self):
        url = reverse('offerdetail-detail')
        data = {
        "title": "Grafikdesign-Paket",
        "image": None,
        "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        "details": [
            {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "basic"
            },
            {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
            },
            {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
            }
        ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_post_NOT_All_Details_400(self):
        url = reverse('offerdetail-detail')
        data = {
        "title": "Grafikdesign-Paket",
        "image": None,
        "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        "details": [
            {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
            },
            {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
            }
        ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_Wrong_type_400(self):
        url = reverse('offerdetail-detail')
        data = {
        "title": "Grafikdesign-Paket",
        "image": None,
        "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        "details": [
            {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "standard"
            },
            {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
            },
            {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
            }
        ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_empty_fields_400(self):
        url = reverse('offerdetail-detail')
        data = {
        "title": "Grafikdesign-Paket",
        "image": None,
        "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        "details": [
            {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price":100,
            "features": [
                "Logo Design",
                "Visitenkarte"
            ],
            "offer_type": "standard"
            },
            {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier"
            ],
            "offer_type": "standard"
            },
            {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features": [
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer"
            ],
            "offer_type": "premium"
            }
        ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)