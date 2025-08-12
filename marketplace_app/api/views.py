from django.contrib.auth import get_user_model
from django.db.models import Min, Q, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import OfferFilter
from .permissions import IsBusiness, IsOfferOwner, IsCustomer, IsReviewer
from .serializers import OfferListReadSerializer, OfferCreateSerializer, OfferRetrieveSerializer, OfferDetailBaseSerializer, OrderListSerializer, OrderDetailSerializer, ReviewListSerializer, ReviewDetailSerializer
from marketplace_app.models import Offer, OfferDetail, Order, Review
from users_app.models import Profile

User = get_user_model()


class OfferListCreateView(generics.ListCreateAPIView):
    """
    View to list and create offers.
    """
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter, filters.SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    search_fields = ['title', 'description']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 1
    pagination_class.page_size_query_param = 'page_size'

    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListReadSerializer

    def get_queryset(self):
        queryset = Offer.objects.all()
        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            queryset = queryset.filter(user__id=creator_id)
        queryset = queryset.annotate(min_price=Min('details__price'))
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsBusiness()]
        else:
            return [permission() for permission in self.permission_classes]


class OfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferRetrieveSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete', 'options', 'head']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOfferOwner(), IsAuthenticated()]
        else:
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OfferCreateSerializer
        else:
            return self.serializer_class


class OfferDetailView(generics.RetrieveAPIView):
    """
    View to retrieve offer details.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailBaseSerializer
    permission_classes = [IsAuthenticated]


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
    http_method_names = ['patch', 'delete', 'options', 'head']

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsBusiness()]
        elif self.request.method == 'DELETE':
            return [IsAdminUser()]


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
        count = Order.objects.filter(business_user=business_user_id).count()
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


class ReviewListCreateView(generics.ListCreateAPIView):
    """
    View to list and create reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsCustomer(), IsAuthenticated()]
        return [IsAuthenticated()]


class ReviewUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to update and delete reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsReviewer, IsAuthenticated]
    http_method_names = ['patch', 'delete', 'options', 'head']


class BaseInfoView(APIView):
    """
    View to retrieve base information.
    """
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        avg = Review.objects.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(avg, 1) if avg is not None else None
        data = {
            "review_count": Review.objects.count(),
            "average_rating": average_rating,
            "business_profile_count": Profile.objects.filter(user__type="business").count(),
            "offer_count": Offer.objects.count()
        }
        return Response(data)
