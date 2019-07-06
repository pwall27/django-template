from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView

from app.serializers import APILoginSerializer, APIRefreshSerializer


class APILoginView(TokenObtainPairView):
    serializer_class = APILoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class APIRefreshView(TokenObtainPairView):
    serializer_class = APIRefreshSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
        serializer = self.get_serializer(data={'refresh_token': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
