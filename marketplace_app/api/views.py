from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .filters import OfferFilter
from .permissions import IsBusiness
from .serializers import OfferReadSerializer, OfferCreateSerializer
from marketplace_app.models import Offer


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
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferReadSerializer

    def get_queryset(self):
        queryset = Offer.objects.all()
        creator_id = self.request.query_params.get('creator_id')
        if creator_id is not None:
            queryset = queryset.filter(user__id=creator_id)
        queryset = queryset.annotate(min_price=Min('details__price'))
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsBusiness()]
        else:
            return [permission() for permission in self.permission_classes]


class OfferDetailView(generics.RetrieveAPIView):
    """
    View to retrieve details of a specific offer.
    """
    # CHANGE IT
    queryset = Offer.objects.all()
    serializer_class = OfferReadSerializer
