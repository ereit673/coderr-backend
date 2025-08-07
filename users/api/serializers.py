from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration and representation.
    Handles validation for password confirmation, unique username/email,
    and enforces user type choices.
    """
    user_id = serializers.IntegerField(source='id', read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    repeated_password = serializers.CharField(write_only=True, required=True)
    type = serializers.ChoiceField(
        choices=[('customer', 'customer'), ('business', 'business')], write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'repeated_password', 'user_id', 'type']

    def validate(self, data):
        """
        Validate that the password and repeated_password match.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError(
                {'repeated_password': "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Create a new user instance with hashed password,
        removing repeated_password from the data.
        """
        validated_data.pop('repeated_password')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
