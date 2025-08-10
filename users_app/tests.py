from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users_app.models import Profile

User = get_user_model()


class AccountTests(APITestCase):
    """
    Tests for user account creation and login functionality.
    Includes tests for successful account creation, missing fields,
    and login with correct and incorrect credentials.
    """

    def setUp(self):
        """
        Create a test user for login tests.
        """
        self.user = User.objects.create_user(
            username="testCustomer",
            email="testCustomer@mail.de",
            password="examplePassword"
        )

    def test_create_account(self):
        """
        Test successful account creation with all required fields.
        Checks if the user is created and the response status is 201.
        """
        url = reverse('registration')
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertTrue(User.objects.filter(
            username='exampleUsername').exists())

    def test_create_account_missing_username(self):
        """
        Test account creation with missing username.
        Should return a 400 status code indicating bad request.
        """
        url = reverse('registration')
        data = {
            # "username" intentionally omitted
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_account(self):
        """
        Test user login with correct credentials.
        Should return a 200 status code and a token in the response.
        """
        url = reverse('login')
        data = {
            "username": "testCustomer",
            "password": "examplePassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data.get('username'), 'testCustomer')

    def test_login_wrong_password(self):
        """
        Test user login with incorrect password.
        Should return a 400 status code indicating bad request.
        """
        url = reverse('login')
        data = {
            "username": "testCustomer",
            "password": "wrongPassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileGetTests(APITestCase):
    """
    Tests for retrieving user profiles.
    Includes tests for successful profile retrieval, unauthenticated access,
    and handling of non-existent profiles.
    """

    def setUp(self):
        """
        Create a test user and profile for profile retrieval tests.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.de",
            password="testpassword"
        )
        Profile.objects.create(user=self.user)
        self.profile_url = reverse(
            'profile', kwargs={'pk': self.user.pk})

    def test_get_profile_success(self):
        """
        Test successful retrieval of a user profile.
        Should return a 200 status code and the profile data.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_unauthenticated(self):
        """
        Test profile retrieval without authentication.
        Should return a 401 status code indicating unauthorized access.
        """
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_not_found(self):
        """
        Test retrieval of a non-existent profile.
        Should return a 404 status code indicating not found.
        """
        self.client.force_authenticate(user=self.user)
        invalid_url = reverse('profile', kwargs={'pk': 9999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profiles_business(self):
        """
        Test retrieval of profiles with business type.
        Should return a 200 status code and the list of profiles.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('business_profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profiles_customer(self):
        """
        Test retrieval of profiles with customer type.
        Should return a 200 status code and the list of profiles.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('customer_profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profiles_business_unauthenticated(self):
        """
        Test retrieval of business profiles without authentication.
        Should return a 401 status code indicating unauthorized access.
        """
        url = reverse('business_profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profiles_customer_unauthenticated(self):
        """
        Test retrieval of customer profiles without authentication.
        Should return a 401 status code indicating unauthorized access.
        """
        url = reverse('customer_profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfilePatchTests(APITestCase):
    """
    Tests for updating user profiles via PATCH requests.
    Includes tests for successful updates, unauthorized access,
    and attempts to update profiles of other users.
    """

    def setUp(self):
        """
        Create test users and profiles for profile update tests.
        """
        self.owner = User.objects.create_user(
            username="owner",
            email="owner@mail.de",
            password="password123"
        )
        self.owner_profile = Profile.objects.create(user=self.owner)
        self.owner_profile_url = reverse(
            'profile', kwargs={'pk': self.owner_profile.pk})

        self.other_user = User.objects.create_user(
            username="other",
            email="other@mail.de",
            password="password123"
        )
        self.other_profile = Profile.objects.create(user=self.other_user)
        self.other_profile_url = reverse(
            'profile', kwargs={'pk': self.other_profile.pk})

    def test_patch_profile_success(self):
        """
        Test successful profile update by the owner.
        Should return a 200 status code and update the profile data.
        """
        self.client.force_authenticate(user=self.owner)
        data = {
            'description': 'Updated description text',
        }
        response = self.client.patch(
            self.owner_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.owner_profile.refresh_from_db()
        self.assertEqual(self.owner_profile.description,
                         'Updated description text')

    def test_patch_profile_unauthenticated(self):
        """
        Test profile update without authentication.
        Should return a 401 status code indicating unauthorized access.
        """
        data = {'description': 'Updated description'}
        response = self.client.patch(
            self.owner_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_forbidden(self):
        """
        Test profile update by a user who is not the owner.
        Should return a 403 status code indicating forbidden access.
        """
        self.client.force_authenticate(user=self.other_user)
        data = {'description': 'Malicious update'}
        response = self.client.patch(
            self.owner_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_not_found(self):
        """
        Test profile update for a non-existent profile.
        Should return a 404 status code indicating not found.
        """
        self.client.force_authenticate(user=self.owner)
        invalid_url = reverse('profile', kwargs={'pk': 9999})
        data = {'bio': 'No update'}
        response = self.client.patch(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
