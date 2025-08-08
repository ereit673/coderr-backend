from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsUserOrReadOnly
from .serializers import UserSerializer, ProfileSerializer
from ..models import Profile

User = get_user_model()


class RegistrationView(APIView):
    """
    API view to handle user registration.

    Accepts POST requests with user data, validates and creates a new user,
    then returns a token for authentication along with the user data.

    Expected input:
        - username
        - email
        - password
        - repeated_password
        - type (customer or business)

    Returns:
        - HTTP 201 with token and user info if successful
        - HTTP 400 with validation errors if input is invalid
    """

    def post(self, request):
        """
        Handle POST request for user registration.

        - Deserialize input data using UserSerializer.
        - Validate the data.
        - Save the new user.
        - Generate or retrieve an auth token for the user.
        - Return the token and serialized user data in the response.
        """

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            token, created = Token.objects.get_or_create(
                user=serializer.instance)
            response_data = {
                'token': token.key,
                **serializer.data
            }
            return Response(response_data, status=201)
        else:
            return Response(serializer.errors, status=400)


class CustomAuthToken(ObtainAuthToken):
    """
    Custom authentication token view.

    This view extends the default ObtainAuthToken to return the user data
    along with the token upon successful login.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for user login.

        - If successful, return the token and user data.
        """

        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response_data = {
            'token': token.key,
            'username': user.username,
            'email': user.email,
            'user_id': user.id
        }
        return Response(response_data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update user profiles.

    Allows authenticated users to view and edit their own profile.
    Other users can only read the profile.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsUserOrReadOnly]
    allowed_methods = ['GET', 'PATCH']

    def get_object(self):
        """
        Retrieve the profile object based on the user ID from the URL.

        Returns:
            Profile instance associated with the user ID.
        """
        user_id = self.kwargs['pk']
        return get_object_or_404(Profile, user__id=user_id)

    def perform_update(self, serializer):
        """
        Save the updated profile instance.

        Ensures that the user has permission to update the profile.
        """
        instance = self.get_object()
        self.check_object_permissions(self.request, instance)
        serializer.save()
