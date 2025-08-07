from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class RegistrationView(APIView):
    def post(self, request):
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
