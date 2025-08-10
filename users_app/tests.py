from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users_app.models import Profile

User = get_user_model()


class AccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testCustomer",
            email="testCustomer@mail.de",
            password="examplePassword"
        )

    def test_create_account(self):
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
        url = reverse('login')
        data = {
            "username": "testCustomer",
            "password": "wrongPassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileGetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.de",
            password="testpassword"
        )
        Profile.objects.create(user=self.user)
        self.profile_url = reverse(
            'profile', kwargs={'pk': self.user.pk})

    def test_get_profile_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_not_found(self):
        self.client.force_authenticate(user=self.user)
        invalid_url = reverse('profile', kwargs={'pk': 9999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProfileGetTests(APITestCase):
    def setUp(self):
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
        data = {'description': 'Updated description'}
        response = self.client.patch(
            self.owner_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        data = {'description': 'Malicious update'}
        response = self.client.patch(
            self.owner_profile_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_not_found(self):
        self.client.force_authenticate(user=self.owner)
        invalid_url = reverse('profile', kwargs={'pk': 9999})
        data = {'bio': 'No update'}
        response = self.client.patch(invalid_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
