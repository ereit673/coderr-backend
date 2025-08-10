from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from marketplace_app.models import OfferDetail

User = get_user_model()


class OfferDetailTests(APITestCase):
    """
    Test cases for OfferDetail API endpoints."""

    def setUp(self):
        self.business_user = User.objects.create_user(
            username='business_user',
            password='password123',
            type='business'
        )
        self.offer = OfferDetail.objects.create(
            title="Test Offer Detail",
            revisions=3,
            delivery_time_in_days=5,
            price=100.00,
            features=["Feature 1", "Feature 2"],
            offer_type="standard"
        )

    def test_get_offer_detail_success(self):
        """
        Test retrieving an offer detail successfully."""
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offerdetails-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Offer Detail")

    def test_get_offer_detail_unauthenticated(self):
        """
        Test retrieving an offer detail without authentication.
        """
        url = reverse('offerdetails-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offer_detail_not_found(self):
        """
        Test retrieving an offer detail that does not exist.
        """
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offerdetails-detail',
                      kwargs={'pk': 9999})  # Non-existent ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
