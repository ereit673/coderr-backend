from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import OfferFilter
from .permissions import IsBusiness, IsOfferOwner
from .serializers import OfferListReadSerializer, OfferCreateSerializer, OfferRetrieveSerializer
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
        return OfferListReadSerializer

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
    queryset = Offer.objects.all()
    serializer_class = OfferListReadSerializer
