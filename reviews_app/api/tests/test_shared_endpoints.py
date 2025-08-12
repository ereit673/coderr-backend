from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from reviews_app.models import Review
from users_app.models import Profile

User = get_user_model()


class SharedEndpointsTests(APITestCase):
    """
    Test suite for shared endpoints.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.url = reverse('base-info')
        self.business_user1 = User.objects.create_user(
            username="business",
            email="business@mail.de",
            password="password123",
            type="business"
        )
        self.business_user2 = User.objects.create_user(
            username="business2",
            email="business2@mail.de",
            password="password123",
            type="business"
        )
        self.business_user3 = User.objects.create_user(
            username="business3",
            email="business3@mail.de",
            password="password123",
            type="business"
        )
        self.customer_user1 = User.objects.create_user(
            username="customer",
            email="customer@mail.de",
            password="password123",
            type="customer"
        )
        self.customer_user2 = User.objects.create_user(
            username="customer2",
            email="customer2@mail.de",
            password="password123",
            type="customer"
        )
        Profile.objects.create(user=self.business_user1)
        Profile.objects.create(user=self.business_user2)
        Profile.objects.create(user=self.business_user3)
        Profile.objects.create(user=self.customer_user1)
        Profile.objects.create(user=self.customer_user2)
        self.review1 = Review.objects.create(
            business_user=self.business_user1,
            reviewer=self.customer_user1,
            rating=5,
            description="Great service!"
        )
        self.review2 = Review.objects.create(
            business_user=self.business_user2,
            reviewer=self.customer_user2,
            rating=4,
            description="Good experience."
        )
        self.review3 = Review.objects.create(
            business_user=self.business_user1,
            reviewer=self.customer_user2,
            rating=5,
            description="Excellent support!"
        )
        self.review4 = Review.objects.create(
            business_user=self.business_user2,
            reviewer=self.customer_user1,
            rating=1,
            description="Terrible experience."
        )
        self.review5 = Review.objects.create(
            business_user=self.business_user3,
            reviewer=self.customer_user1,
            rating=5,
            description="Fantastic service!"
        )
        self.review6 = Review.objects.create(
            business_user=self.business_user3,
            reviewer=self.customer_user2,
            rating=2,
            description="Not great."
        )
        self.offer1 = Offer.objects.create(
            user=self.business_user1,
            title="Test Offer",
            image=None,
            description="This is a test offer for unit testing."
        )
        self.offer_detail1 = OfferDetail.objects.create(
            offer=self.offer1,
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
        self.offer_detail2 = OfferDetail.objects.create(
            offer=self.offer1,
            title="Standard Test Package",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=[
                "Test Feature C",
                "Test Feature D",
                "Test Feature E"
            ],
            offer_type="standard"
        )
        self.offer_detail3 = OfferDetail.objects.create(
            offer=self.offer1,
            title="Premium Test Package",
            revisions=5,
            delivery_time_in_days=7,
            price=300,
            features=[
                "Test Feature F",
                "Test Feature G",
                "Test Feature H",
                "Test Feature I"
            ],
            offer_type="premium"
        )
        self.offer2 = Offer.objects.create(
            user=self.business_user2,
            title="Another Test Offer",
            image=None,
            description="This is another test offer for unit testing."
        )
        self.offer_detail4 = OfferDetail.objects.create(
            offer=self.offer2,
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
        self.offer_detail5 = OfferDetail.objects.create(
            offer=self.offer2,
            title="Standard Test Package",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=[
                "Test Feature C",
                "Test Feature D",
                "Test Feature E"
            ],
            offer_type="standard"
        )
        self.offer_detail6 = OfferDetail.objects.create(
            offer=self.offer2,
            title="Premium Test Package",
            revisions=5,
            delivery_time_in_days=7,
            price=300,
            features=[
                "Test Feature F",
                "Test Feature G",
                "Test Feature H",
                "Test Feature I"
            ],
            offer_type="premium"
        )

    def test_get_base_info(self):
        """
        Test retrieving base information.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('review_count', response.data)
        self.assertIn('offer_count', response.data)
        self.assertIn('business_profile_count', response.data)
        self.assertIn('offer_count', response.data)
        self.assertEqual(response.data['review_count'], 6)
        self.assertEqual(response.data['average_rating'], 3.7)
        self.assertEqual(response.data['business_profile_count'], 3)
        self.assertEqual(response.data['offer_count'], 2)
