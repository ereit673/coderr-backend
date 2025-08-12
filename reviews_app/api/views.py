from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from offers_app.models import Offer
from reviews_app.api.permissions import IsCustomer, IsReviewer
from reviews_app.api.serializers import ReviewListSerializer, ReviewDetailSerializer
from reviews_app.models import Review
from users_app.models import Profile

User = get_user_model()


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
