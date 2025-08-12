import django_filters

from django.db.models import Min
from rest_framework.exceptions import ValidationError

from marketplace_app.models import Offer


class OfferFilter(django_filters.FilterSet):
    """
    Filter for offers based on minimum price and maximum delivery time.
    """
    creator_id = django_filters.NumberFilter(field_name='user__id')
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_delivery_time = django_filters.NumberFilter(
        method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']

    def filter_min_price(self, queryset, name, value):
        if value in [None, '']:
            return queryset
        return queryset.filter(details__price=value)

    def filter_max_delivery_time(self, queryset, name, value):
        if value in [None, '']:
            return queryset
        annotated_queryset = queryset.annotate(
            _min_delivery_time=Min('details__delivery_time_in_days'))
        return annotated_queryset.filter(_min_delivery_time__lte=value)

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset)
