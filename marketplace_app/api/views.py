from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .serializers import OfferReadSerializer, OfferCreateSerializer
from marketplace_app.models import Offer


class OfferListCreateView(generics.ListCreateAPIView):
    """
    View to list and create offers.
    """
    queryset = Offer.objects.all()
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferReadSerializer


class OfferDetailView(generics.RetrieveAPIView):
    """
    View to retrieve details of a specific offer.
    """
    # CHANGE IT
    queryset = Offer.objects.all()
    serializer_class = OfferReadSerializer
