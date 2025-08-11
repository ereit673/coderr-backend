from urllib.parse import urlparse

from django.db.models import Min
from rest_framework import serializers

from marketplace_app.models import Offer, OfferDetail, Order, Review
from users_app.models import Profile


class RelativeHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """
    Custom field to return a relative URL instead of an absolute one.
    """

    def to_representation(self, value):
        full_url = super().to_representation(value)
        parsed = urlparse(full_url)
        path = parsed.path
        if path.startswith('/api'):
            path = path[len('/api'):]
        return path


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for user details in the Offer model.
    """
    username = serializers.CharField(max_length=255, source='user.username')

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'username'
        ]


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating OfferDetail with price validation.
    """
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
        ]


class OfferDetailReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading OfferDetail with a relative URL.
    """
    url = RelativeHyperlinkedIdentityField(
        view_name='offerdetails-detail',
        lookup_field='pk'
    )

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'url'
        ]


class OfferReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Offer details with nested OfferDetails.
    """
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source='user.profile', read_only=True)
    details = OfferDetailReadSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price'] or 0

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery_time=Min('delivery_time_in_days'))['min_delivery_time']


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an Offer with nested OfferDetails.
    """
    details = OfferDetailCreateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image',
            'description',
            'details'
        ]

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
