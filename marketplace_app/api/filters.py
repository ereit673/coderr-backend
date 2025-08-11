import django_filters
from marketplace_app.models import Offer
from django.db.models import Min


class OfferFilter(django_filters.FilterSet):
    """
    Filter for offers based on minimum price and maximum delivery time.
    """
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_delivery_time = django_filters.NumberFilter(
        method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['min_price', 'max_delivery_time']

    def filter_min_price(self, queryset, name, value):
        if value is not None:
            return queryset.filter(details__price=value)
        return queryset

    def filter_max_delivery_time(self, queryset, name, value):
        if value is not None:
            queryset = queryset.annotate(
                _min_delivery_time=Min('details__delivery_time_in_days'))
            return queryset.filter(_min_delivery_time__lte=value)
        return queryset
