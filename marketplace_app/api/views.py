from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .serializers import OfferSerializer
from marketplace_app.models import Offer


class OfferListCreateView(generics.ListCreateAPIView):
    """
    View to list and create offers.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
