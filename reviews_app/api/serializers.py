from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from reviews_app.models import Review


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
