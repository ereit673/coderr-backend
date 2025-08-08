from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import Profile

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
        Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile representation.
    Excludes password and repeated_password fields.
    """
    user = serializers.IntegerField(source='user.id', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Profile
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
            'email',
            'created_at'
        ]

    def validate_email(self, value):
        """
        Validate that the email is unique across all users.
        """
        user = self.instance.user if self.instance else None
        if user and user.email == value:
            return value
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def update(self, instance, validated_data):
        """
        Update the profile instance with validated data.
        """
        email_data = validated_data.pop('user', {}).get('email')
        if email_data and email_data != instance.user.email:
            instance.user.email = email_data
            instance.user.save()

        file = validated_data.get('file')
        if file:
            instance.file = file

        for attr in ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']:
            setattr(instance, attr, validated_data.get(
                attr, getattr(instance, attr)))

        instance.save()
        return instance


class BusinessListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing business profiles.
    Includes only essential fields for business profiles.
    """
    user = serializers.IntegerField(source='user.id', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type"
        ]


class CustomerListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing customer profiles.
    Includes only essential fields for customer profiles.
    """
    user = serializers.IntegerField(source='user.id', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "uploaded_at",
            "type"
        ]
