
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from orders_app.models import Order, OfferDetail


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
