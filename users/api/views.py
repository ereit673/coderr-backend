from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


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
