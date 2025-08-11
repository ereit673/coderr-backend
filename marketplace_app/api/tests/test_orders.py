from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from marketplace_app.models import Order, OfferDetail, Offer
from users_app.models import Profile

User = get_user_model()


class OrdersGetPostTests(APITestCase):
    def setUp(self):
        self.url = reverse('orders-list')
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

        offer = Offer.objects.create(
            title="Test Offer",
            image=None,
            description="Test offer description",
            user=self.business_user
        )
        for offer_type in ["basic", "standard", "premium"]:
            offer_detail = OfferDetail.objects.create(
                offer=offer,
                title=offer_type.capitalize(),
                revisions=1,
                delivery_time_in_days=3,
                price=50,
                features=["A", "B"],
                offer_type=offer_type
            )
            if offer_type == "basic":
                self.offer_detail_id = offer_detail.id

    def test_get_orders_successful(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        if response.data:
            expected_keys = {'id', 'customer_user', 'business_user', 'title', 'revisions',
                             'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at'}
            self.assertTrue(expected_keys.issubset(response.data[0].keys()))

    def test_get_orders_not_authenticated(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_order_successful(self):
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "offer_detail_id": self.offer_id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_order_offer_id_missing(self):
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "offer": self.offer_id  # wrong key name
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_not_authenticated(self):
        data = {
            "offer_detail_id": self.offer_id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_wrong_user_type(self):
        self.client.force_authenticate(user=self.business_user)
        data = {
            "offer_detail_id": self.offer_id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_order_wrong_offer_id(self):
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "offer_detail_id": self.offer_id + 99999  # wrong offer_id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrdersPatchDeleteTests(APITestCase):
    def setUp(self):
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
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )

        self.offer = Offer.objects.create(
            title="Test Offer",
            image=None,
            description="Test offer description",
            user=self.business_user
        )
        for offer_type in ["basic", "standard", "premium"]:
            offer_detail = OfferDetail.objects.create(
                offer=self.offer,
                title=offer_type.capitalize(),
                revisions=1,
                delivery_time_in_days=3,
                price=50,
                features=["A", "B"],
                offer_type=offer_type
            )
            if offer_type == "basic":
                self.offer_detail_id = offer_detail.id

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer=self.offer.details.first(),
            status='in_progress',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        self.url = reverse('orders-detail', kwargs={'pk': self.order.id})

    def test_patch_order_successful(self):
        self.client.force_authenticate(user=self.business_user)
        data = {
            "status": "completed"
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    def test_patch_order_wrong_key(self):
        self.client.force_authenticate(user=self.business_user)
        data = {
            "revisions": 1
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_not_authenticated(self):
        data = {
            "status": "completed"
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_order_wrong_user_type(self):
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "status": "completed"
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_not_found(self):
        wrong_url = reverse(
            'orders-detail', kwargs={'pk': self.order.id + 99999})
        self.client.force_authenticate(user=self.customer_user)
        data = {
            "status": "completed"
        }
        response = self.client.patch(wrong_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_successful(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_not_authenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_order_not_admin(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_not_found(self):
        wrong_url = reverse(
            'orders-detail', kwargs={'pk': self.order.id + 99999})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(wrong_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrdersExtraTests(APITestCase):
    def setUp(self):
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
        self.offer = Offer.objects.create(
            title="Test Offer",
            image=None,
            description="Test offer description",
            user=self.business_user
        )
        offer_details = {}
        for offer_type in ["basic", "standard", "premium"]:
            offer_detail = OfferDetail.objects.create(
                offer=self.offer,
                title=offer_type.capitalize(),
                revisions=1,
                delivery_time_in_days=3,
                price=50,
                features=["A", "B"],
                offer_type=offer_type
            )
            offer_details[offer_type] = offer_detail

        self.offer_detail_basic = offer_details["basic"]
        self.offer_detail_standard = offer_details["standard"]

        self.order_1 = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer=self.offer_detail_basic,
            status='completed',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        self.order_2 = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            offer=self.offer_detail_standard,
            status='completed',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    def test_get_order_count_successful(self):
        url = reverse(
            'order-count', kwargs={'business_user_id': self.business_user.id})
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 2)

    def test_get_order_count_not_authenticated(self):
        url = reverse(
            'order-count', kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_count_wrong_user_id(self):
        url = reverse(
            'order-count', kwargs={'business_user_id': self.business_user.id + 999999})
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_completed_order_count_successful(self):
        url = reverse('completed-orders',
                      kwargs={'business_user_id': self.business_user.id})
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 2)

    def test_get_completed_order_count_not_authenticated(self):
        url = reverse('completed-orders',
                      kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_completed_order_count_not_found(self):
        url = reverse('completed-orders',
                      kwargs={'business_user_id': self.business_user.id + 999999})
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
