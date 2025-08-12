from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from reviews_app.models import Review
from users_app.models import Profile

User = get_user_model()


class ReviewsGetPostTests(APITestCase):
    """
    Test suite for getting and creating reviews.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.url = reverse('reviews-list')
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
        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=5,
            description='Test description'
        )

    def test_get_reviews_successful(self):
        """
        Test getting reviews as a authenticated user. 
        """
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_reviews_not_authorized(self):
        """
        Test getting reviews as an unauthenticated user.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_review_successful(self):
        """
        Test posting a review as a customer user.
        """
        business_user = User.objects.create_user(
            username="business2",
            email="business2@mail.de",
            password="password123",
            type="business"
        )
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "business_user": business_user.id,
            "rating": 5,
            "description": "Test description"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_missing_fields(self):
        """
        Test posting a review with missing fields.
        """
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "business_user": self.business_user.id,
            # "rating": missing
            "description": "Test description"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_not_authenticated(self):
        """
        Test posting a review as an unauthenticated user.
        """
        data = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Test description"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_more_than_one_review(self):
        """
        Test posting more than one review as a customer user.
        """
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Test description"
        }
        self.client.post(self.url, data, format='json')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewsPatchDeleteTests(APITestCase):
    """
    Test suite for updating and deleting reviews.
    """

    def setUp(self):
        """
        Set up the test case.
        """
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
        self.old_review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=5,
            description='Test description'
        )
        self.url = reverse('reviews-detail', kwargs={'pk': self.old_review.id})

    def test_patch_review_successful(self):
        """
        Test patching a review as the owner.
        """
        data = {
            "rating": 3,
            "description": "Updated description"
        }
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.old_review.refresh_from_db()
        self.assertEqual(self.old_review.rating, 3)
        self.assertEqual(self.old_review.description, "Updated description")

    def test_patch_review_wrong_fields(self):
        """
        Test patching a review with wrong fields.
        """
        data = {
            "business_user": 5
        }
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_review_not_authenticated(self):
        """
        Test patching a review as an unauthenticated user.
        """
        data = {
            "rating": 3,
            "description": "Updated description"
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_review_another_customer(self):
        """
        Test patching a review as another customer user.
        """
        customer_user2 = User.objects.create(
            username="customer2",
            email="customer2@mail.de",
            password="password123",
            type="customer"
        )
        self.client.force_authenticate(user=customer_user2)
        data = {
            "rating": 3,
            "description": "Updated description"
        }
        response = self.client.patch(self.url, data, content_type='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_review_not_found(self):
        """
        Test patching a review that does not exist.
        """
        wrong_url = reverse(
            'reviews-detail', kwargs={'pk': self.old_review.id + 99999})
        data = {
            "rating": 3,
            "description": "Updated description"
        }
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.patch(wrong_url, data, content_type='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_review_successful(self):
        """
        Test deleting a review as the owner.
        """
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_authenticated(self):
        """
        Test deleting a review as an unauthenticated user.
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_review_another_customer(self):
        """
        Test deleting a review as another customer user.
        """
        customer_user2 = User.objects.create(
            username="customer2",
            email="customer2@mail.de",
            password="password123",
            type="customer"
        )
        self.client.force_authenticate(user=customer_user2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_not_found(self):
        """
        Test deleting a review that does not exist.
        """
        wrong_url = reverse(
            'reviews-detail', kwargs={'pk': self.old_review.id + 99999})
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(wrong_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
