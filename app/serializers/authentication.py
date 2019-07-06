from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type


class APILoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(TokenObtainPairSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)

        data['access_token'] = text_type(refresh.access_token)
        data['refresh_token'] = text_type(refresh)

        return data


class APIRefreshSerializer(serializers.Serializer):

    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):

        refresh = RefreshToken(attrs['refresh_token'])

        data = {'access_token': text_type(refresh.access_token)}

        return data
