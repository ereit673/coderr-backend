from django.contrib.auth import get_user_model
from django.db.models import Q


from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from orders_app.api.serializers import OrderListSerializer, OrderDetailSerializer
from orders_app.api.permissions import IsOrderBusinessUser, IsCustomer
from orders_app.models import Order

User = get_user_model()


class OrderListCreateView(generics.ListCreateAPIView):
    """
    View to list and create orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomer(), IsAuthenticated()]
        return [permission() for permission in self.permission_classes]


class OrderUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to update and delete orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer

    def get(self, request, *args, **kwargs):
        return Response({'detail': 'Method \"GET\" not allowed.'}, status=405)

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        else:
            return [IsOrderBusinessUser()]


class OrderCountView(APIView):
    """
    View to retrieve the order count for a business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, format=None):
        try:
            User.objects.get(id=business_user_id, type='business')
        except User.DoesNotExist:
            raise NotFound("Business user with this id does not exist.")
        count = Order.objects.filter(
            business_user=business_user_id, status='in_progress').count()
        return Response({'order_count': count})


class OrderCompleteCount(APIView):
    """
    View to retrieve the completed order count for a business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id, format=None):
        try:
            User.objects.get(id=business_user_id, type='business')
        except User.DoesNotExist:
            raise NotFound("Business user with this id does not exist.")
        count = Order.objects.filter(
            business_user=business_user_id, status="completed").count()
        return Response({'completed_order_count': count})
