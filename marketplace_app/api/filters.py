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
        if value is not None:
            filtered_queryset = queryset.filter(details__price=value)
            if not filtered_queryset.exists():
                raise ValidationError(
                    {'min_price': f'No offers found with that price.'})
            return filtered_queryset
        return queryset

    def filter_max_delivery_time(self, queryset, name, value):
        if value is not None:
            annotated_queryset = queryset.annotate(
                _min_delivery_time=Min('details__delivery_time_in_days'))
            filtered_queryset = annotated_queryset.filter(
                _min_delivery_time__lte=value)
            if not filtered_queryset.exists():
                raise ValidationError(
                    {'max_delivery_time': f'No offers found with delivery time <= {value}.'})
            return filtered_queryset
        return queryset

    def filter_queryset(self, queryset):
        filtered_queryset = super().filter_queryset(queryset)

        creator_id = self.data.get('creator_id')
        if creator_id and not filtered_queryset.exists():
            raise ValidationError(
                {'creator_id': f'No offers found for creator with id {creator_id}.'})

        return filtered_queryset
