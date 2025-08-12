from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from marketplace_app.models import Offer, OfferDetail
from users_app.models import Profile

User = get_user_model()


class OffersGetPostTests(APITestCase):
    """
    Test cases for Offer List and Create API endpoints.
    """

    def setUp(self):
        """
        Set up test data for Offer List and Create tests.
        """
        self.url = reverse('offers-list')
        self.business_user = User.objects.create_user(
            username="business",
            email="business@mail.de",
            password="password123",
            type="business"
        )
        Profile.objects.create(user=self.business_user)
        self.customer_user = User.objects.create_user(
            username="customer",
            email="customer@mail.de",
            password="password123",
            type="customer"
        )
        Profile.objects.create(user=self.customer_user)

    def test_get_offers_success(self):
        """
        Test retrieving offers successfully.
        """
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_offer_success(self):
        """
        Test creating an offer successfully.
        """
        self.client.force_authenticate(user=self.business_user)
        data = {
            "title": "Test Offer Title",
            "image": None,
            "description": "This is a test offer description for unit testing.",
            "details": [
                {
                    "title": "Basic Test Package",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": 50,
                    "features": [
                        "Test Feature A",
                        "Test Feature B"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Test Package",
                    "revisions": 3,
                    "delivery_time_in_days": 5,
                    "price": 150,
                    "features": [
                        "Test Feature C",
                        "Test Feature D",
                        "Test Feature E"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Test Package",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 300,
                    "features": [
                        "Test Feature F",
                        "Test Feature G",
                        "Test Feature H",
                        "Test Feature I"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

    def test_post_offer_unauthenticated(self):
        """
        Test creating an offer without authentication.
        """
        data = {
            "title": "Test Offer Title",
            "image": None,
            "description": "This is a test offer description for unit testing.",
            "details": [
                {
                    "title": "Basic Test Package",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": 50,
                    "features": [
                        "Test Feature A",
                        "Test Feature B"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Test Package",
                    "revisions": 3,
                    "delivery_time_in_days": 5,
                    "price": 150,
                    "features": [
                        "Test Feature C",
                        "Test Feature D",
                        "Test Feature E"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Test Package",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 300,
                    "features": [
                        "Test Feature F",
                        "Test Feature G",
                        "Test Feature H",
                        "Test Feature I"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_offer_invalid_data(self):
        """
        Test creating an offer with invalid data.
        """
        self.client.force_authenticate(user=self.business_user)
        data = {
            # title is missing
            "image": None,
            "description": "This is a test offer description for unit testing.",
            "details": [
                {
                    "title": "Basic Test Package",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": 50,
                    "features": [
                        "Test Feature A",
                        "Test Feature B"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Test Package",
                    "revisions": 3,
                    "delivery_time_in_days": 5,
                    "price": 150,
                    "features": [
                        "Test Feature C",
                        "Test Feature D",
                        "Test Feature E"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Test Package",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 300,
                    "features": [
                        "Test Feature F",
                        "Test Feature G",
                        "Test Feature H",
                        "Test Feature I"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_invalid_user_type(self):
        """
        Test creating an offer as a user who is not a business.
        """
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "title": "Test Offer Title",
            "image": None,
            "description": "This is a test offer description for unit testing.",
            "details": [
                {
                    "title": "Basic Test Package",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": 50,
                    "features": [
                        "Test Feature A",
                        "Test Feature B"
                    ],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Test Package",
                    "revisions": 3,
                    "delivery_time_in_days": 5,
                    "price": 150,
                    "features": [
                        "Test Feature C",
                        "Test Feature D",
                        "Test Feature E"
                    ],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Test Package",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 300,
                    "features": [
                        "Test Feature F",
                        "Test Feature G",
                        "Test Feature H",
                        "Test Feature I"
                    ],
                    "offer_type": "premium"
                }
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OffersRetrieveUpdateDeleteTests(APITestCase):
    """
    Test cases for Offer Retrieve, Update, and Delete API endpoints.
    """

    def setUp(self):
        self.url = reverse('offers-list')
        self.business_user = User.objects.create_user(
            username="business",
            email="businee@email.com",
            password="password123",
            type="business"
        )
        Profile.objects.create(user=self.business_user)
        self.customer_user = User.objects.create_user(
            username="customer",
            email="customer@email.com",
            password="password123",
            type="customer"
        )
        Profile.objects.create(user=self.customer_user)

        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Test Offer",
            image=None,
            description="This is a test offer for unit testing."
        )
        self.offer_id = self.offer.id

        self.offer_details_1 = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Test Package",
            revisions=1,
            delivery_time_in_days=3,
            price=50,
            features=[
                "Test Feature A",
                "Test Feature B"
            ],
            offer_type="basic"
        )
        self.offer_details_2 = OfferDetail.objects.create(
            offer=self.offer,
            title="Standard Test Package",
            revisions=3,
            delivery_time_in_days=5,
            price=120,
            features=[
                "Test Feature A",
                "Test Feature B",
                "Test Feature C"
            ],
            offer_type="standard"
        )

        self.offer_details_3 = OfferDetail.objects.create(
            offer=self.offer,
            title="Premium Test Package",
            revisions=7,
            delivery_time_in_days=7,
            price=250,
            features=[
                "Test Feature A",
                "Test Feature B",
                "Test Feature C",
                "Test Feature D"
            ],
            offer_type="premium"
        )

        self.offer_data = {
            "title": "Test Offer",
            "image": None,
            "description": "This is a test offer for unit testing.",
            "details": [
                {
                    "title": "Basic Test Package",
                    "revisions": 1,
                    "delivery_time_in_days": 3,
                    "price": 50,
                    "features": ["Test Feature A", "Test Feature B"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Test Package",
                    "revisions": 3,
                    "delivery_time_in_days": 5,
                    "price": 120,
                    "features": ["Test Feature A", "Test Feature B", "Test Feature C"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Test Package",
                    "revisions": 7,
                    "delivery_time_in_days": 7,
                    "price": 250,
                    "features": ["Test Feature A", "Test Feature B", "Test Feature C", "Test Feature D"],
                    "offer_type": "premium"
                }
            ]
        }

    def test_get_offer_detail_success(self):
        """
        Test retrieving offer details successfully.
        """
        self.client.force_authenticate(user=self.business_user)
        detail_url = reverse('offers-detail', kwargs={'pk': self.offer_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.offer_data['title'])

    def test_get_offer_detail_unauthenticated(self):
        """
        Test retrieving offer details without authentication.
        """
        detail_url = reverse('offers-detail', kwargs={'pk': self.offer_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

    def test_get_offer_detail_invalid_id(self):
        """
        Test retrieving offer details with an invalid ID.
        """
        self.client.force_authenticate(user=self.business_user)
        detail_url = reverse('offers-detail', kwargs={'pk': 9999999})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_offer_success(self):
        """
        Test updating an offer successfully.
        """
        self.client.force_authenticate(user=self.business_user)
        detail_url = reverse('offers-detail', kwargs={'pk': self.offer_id})
        updated_data = self.offer_data.copy()
        updated_data['title'] = "Updated Offer Title"
        response = self.client.patch(detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], updated_data['title'])

    def test_update_offer_unauthenticated(self):
        """
        Test updating an offer without authentication.
        """
        detail_url = reverse('offers-detail', kwargs={'pk': self.offer_id})
        response = self.client.put(detail_url, self.offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_offer_user_not_owner(self):
        """
        Test updating an offer as a user who is not the owner.
        """
        self.client.force_authenticate(user=self.customer_user)
        detail_url = reverse('offers-detail', kwargs={'pk': self.offer_id})
        response = self.client.patch(
            detail_url, self.offer_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_success(self):
        """
        Test deleting an offer successfully.
        """
        self.client.force_authenticate(user=self.business_user)
        detail_url = reverse('offers-detail', kwargs={'pk': self.offer_id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_offer_unauthenticated(self):
        """
        Test deleting an offer without authentication.
        """
        detail_url = reverse('offers-detail', kwargs={'pk': self.offer_id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_offer_user_not_owner(self):
        """
        Test deleting an offer as a user who is not the owner.
        """
        self.client.force_authenticate(user=self.customer_user)
        detail_url = reverse('offers-detail', kwargs={'pk': self.offer_id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_invalid_id(self):
        """
        Test deleting an offer with an invalid ID.
        """
        self.client.force_authenticate(user=self.business_user)
        detail_url = reverse('offers-detail', kwargs={'pk': 9999999})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
