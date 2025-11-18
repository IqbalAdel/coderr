
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from ..models import Offer, OfferDetail
from ..api.serializers import OfferListSerializer, OffersDetailSerializer, DetailSerializer
from profile_app.models import Profile

class PatchOfferTests(APITestCase):
    
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
        factory = APIRequestFactory()
        self.request = factory.get('/')  
        self.request.user = self.user

        self.client = APIClient()
        self.token = Token.objects.create(user = self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ self.token.key)
        self.offer = Offer.objects.create(
            user=self.user, 
            title='Test-offer1', 
            image= None,
            description='This is a test offer',
            )
        self.offer2 = Offer.objects.create(
            user=self.user2, 
            title='Test-offer2', 
            image= None,
            description='This is a test offer2',
            )
        detail_data = [
            {'title': 'Detail 1', 'revisions': 2, 'delivery_time_in_days': 7, 'price': 100, 'features': ['feature1', 'feature2'], 'offer_type': 'basic'},
            {'title': 'Detail 2', 'revisions': 4, 'delivery_time_in_days': 10, 'price': 200, 'features': ['feature1', 'feature2'], 'offer_type': 'standard'},
            {'title': 'Detail 3', 'revisions': 6, 'delivery_time_in_days': 15, 'price': 300, 'features': ['feature1', 'feature2'], 'offer_type': 'premium'},
    ]
        detail_data2 = [
            {'title': 'Detail 4', 'revisions': 5, 'delivery_time_in_days': 2, 'price': 10, 'features': ['feature1', 'feature2'], 'offer_type': 'basic'},
            {'title': 'Detail 5', 'revisions': 5, 'delivery_time_in_days': 2, 'price': 20, 'features': ['feature1', 'feature2'], 'offer_type': 'standard'},
            {'title': 'Detail 6', 'revisions': 5, 'delivery_time_in_days': 2, 'price': 30, 'features': ['feature1', 'feature2'], 'offer_type': 'premium'},
    ]

        self.details = [
            OfferDetail.objects.create(offer=self.offer, **d)
            for d in detail_data
    ]
        self.details2 = [
            OfferDetail.objects.create(offer=self.offer2, **d)
            for d in detail_data2
    ]
        
    def test_get_offer_200(self):
        url = reverse('offerdetails-detail', kwargs={'pk': self.details[0].id})
        response = self.client.get(url)
        expected_data = DetailSerializer(
                            self.details[0],
                            context={"request": self.request}
                        ).data
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offer_notfound_404(self):
        url = reverse('offerdetails-detail', kwargs={'pk': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_offer_UNAUTH_401(self):
        url = reverse('offerdetails-detail', kwargs={'pk': self.details[0].id})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)