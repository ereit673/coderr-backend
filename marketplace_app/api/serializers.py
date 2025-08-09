from django.db.models import Min

from rest_framework import serializers

from marketplace_app.models import Offer, OfferDetail, Order, Review
from users_app.models import Profile


class UserDetailsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, source='user.username')

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'username'
        ]


class OfferDetailSerializer(serializers.ModelSerializer):
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


class OfferSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source='user.profile', read_only=True)
    details = OfferDetailSerializer(many=True)

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
        ready_only_fields = [
            'id',
            'created_at',
            'updated_at',

        ]

    def get_min_price(self, obj):
        return obj.details.aggregate(min_price=Min('price'))['min_price'] or 0

    def get_min_delivery_time(self, obj):
        return obj.details.aggregate(min_delivery_time=Min('delivery_time_in_days'))['min_delivery_time']

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
