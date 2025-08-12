from urllib.parse import urlparse

from django.db.models import Min
from rest_framework import serializers
from rest_framework.exceptions import NotFound, PermissionDenied

from marketplace_app.models import Offer, OfferDetail, Order, Review
from users_app.models import Profile


class RelativeHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """
    Custom field to return a relative URL instead of an absolute one.
    """

    def to_representation(self, value):
        """
        Override the to_representation method to customize the output.
        """
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


class OfferDetailBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for OfferDetail, used for creating or showing details.
    It includes fields necessary for creating an offer detail.
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


class OfferDetailReadSerializerHyperlink(serializers.ModelSerializer):
    """
    Serializer for reading OfferDetail with a hyperlink.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='offerdetails-detail',
        lookup_field='pk'
    )

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'url'
        ]


class OfferDetailReadSerializerRelativeHyperlinked(serializers.ModelSerializer):
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


class OfferListReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading Offer details with nested OfferDetails.
    """
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = UserDetailsSerializer(source='user.profile', read_only=True)
    details = OfferDetailReadSerializerRelativeHyperlinked(
        many=True, read_only=True)

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
        """
        Get the minimum price from the offer details.
        """
        return obj.details.aggregate(min_price=Min('price'))['min_price'] or 0

    def get_min_delivery_time(self, obj):
        """
        Get the minimum delivery time from the offer details.
        """
        return obj.details.aggregate(min_delivery_time=Min('delivery_time_in_days'))['min_delivery_time']


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an Offer with nested OfferDetails.
    """
    details = OfferDetailBaseSerializer(many=True, required=False)

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
        """
        Create a new offer.
        """
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer

    def update(self, instance, validated_data):
        """
        Update an existing offer.
        """
        details_data = validated_data.pop('details', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        if details_data is not None:
            self.update_details(instance, details_data)
        return instance

    def update_details(self, instance, details_data):
        """
        Update the offer details.
        """
        existing_details = {}
        for detail in instance.details.all():
            key = detail.offer_type
            value = detail
            existing_details[key] = value
        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            if not offer_type or offer_type not in existing_details:
                raise serializers.ValidationError(
                    f"Invalid or missing offer_type: {offer_type}")
            detail_instance = existing_details[offer_type]
            for field_name, field_value in detail_data.items():
                setattr(detail_instance, field_name, field_value)
            detail_instance.save()


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving an Offer with its details.
    """
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    details = OfferDetailReadSerializerHyperlink(many=True, read_only=True)

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
            'min_delivery_time'
        ]

    def get_min_price(self, obj):
        """
        Get the minimum price from the offer details.
        """
        return obj.details.aggregate(min_price=Min('price'))['min_price'] or 0

    def get_min_delivery_time(self, obj):
        """
        Get the minimum delivery time from the offer details.
        """
        return obj.details.aggregate(min_delivery_time=Min('delivery_time_in_days'))['min_delivery_time']


class OrderListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing and creating orders.
    """
    title = serializers.CharField(source='offer.title', read_only=True)
    revisions = serializers.IntegerField(
        source='offer.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(
        source='offer.delivery_time_in_days', read_only=True)
    price = serializers.FloatField(source='offer.price', read_only=True)
    features = serializers.JSONField(source='offer.features', read_only=True)
    offer_type = serializers.CharField(
        source='offer.offer_type', read_only=True)
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source='offer', queryset=OfferDetail.objects.all())

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
            'offer_detail_id'
        ]
        read_only_fields = [
            'id',
            'customer_user',
            'business_user',
            'status',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        """
        Create a new order.
        """
        offer = validated_data['offer']
        customer_user = self.context['request'].user
        business_user = offer.offer.user
        return Order.objects.create(customer_user=customer_user, business_user=business_user, offer=offer)

    def to_internal_value(self, data):
        """
        Validate the incoming data for order creation.
        """
        try:
            return super().to_internal_value(data)
        except serializers.ValidationError as exception:
            if 'offer_detail_id' in exception.detail:
                errors = exception.detail['offer_detail_id']
                for error in errors:
                    error_text = str(error)
                    if 'Invalid pk' in error_text or 'does not exist' in error_text:
                        raise NotFound(detail="Offer not found")
            raise


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for patching orders.
    """
    title = serializers.CharField(source='offer.title', read_only=True)
    revisions = serializers.IntegerField(
        source='offer.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(
        source='offer.delivery_time_in_days', read_only=True)
    price = serializers.FloatField(source='offer.price', read_only=True)
    features = serializers.JSONField(source='offer.features', read_only=True)
    offer_type = serializers.CharField(
        source='offer.offer_type', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'customer_user',
            'business_user',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        """
        Validate the incoming data for order updates.
        """
        if not self.initial_data:
            raise serializers.ValidationError(
                "You must provide at least one field to update."
            )
        for field in self.initial_data:
            if field != 'status':
                raise serializers.ValidationError(
                    "You can only update the 'status' field."
                )
        return attrs


class ReviewListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing reviews and creating.
    """
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'reviewer',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        """
        Create a new review.
        Checks if the business user is valid and if the reviewer has already reviewed the business.
        """
        reviewer = self.context['request'].user
        business_user = validated_data['business_user']
        if business_user.type != 'business':
            raise serializers.ValidationError(
                "You can only review business users.")
        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise PermissionDenied("You have already reviewed this business.")
        validated_data['reviewer'] = reviewer
        return super().create(validated_data)


class ReviewDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving and updating reviews.
    """
    class Meta:
        model = Review
        fields = [
            'id',
            'business_user',
            'reviewer',
            'rating',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'business_user',
            'reviewer',
            'created_at',
            'updated_at'
        ]

    def validate(self, attrs):
        """
        Validate the incoming data for review updates.
        """
        if not self.initial_data:
            raise serializers.ValidationError(
                "You must provide at least one field to update."
            )
        for field in self.initial_data:
            if field not in ['rating', 'description']:
                raise serializers.ValidationError(
                    "You can only update the rating or the description."
                )
        return attrs
