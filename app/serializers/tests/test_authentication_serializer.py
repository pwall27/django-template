import pytest
from faker import Faker
from mixer.backend.django import mixer

from app.serializers import APILoginSerializer, APIRefreshSerializer

fake = Faker()


@pytest.mark.django_db
class TestAPILoginSerializer:
    def test_authentication_serializer(self):
        email = fake.email()
        password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

        user = mixer.blend('app.User', email=email)
        user.set_password(password)
        user.save()

        data = {
            'email': email,
            'password': password
        }

        serializer = APILoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data['access_token']
        assert serializer.validated_data['refresh_token']


@pytest.mark.django_db
class TestAPIRefreshSerializer:
    def test_refresh_serializer(self):
        email = fake.email()
        password = fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

        user = mixer.blend('app.User', email=email)
        user.set_password(password)
        user.save()

        data = {
            'email': email,
            'password': password
        }

        serializer = APILoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data['access_token']
        assert serializer.validated_data['refresh_token']

        refresh_token = serializer.validated_data['refresh_token']

        serializer = APIRefreshSerializer(data={'refresh_token': refresh_token})
        serializer.is_valid(raise_exception=True)
        assert serializer.validated_data['access_token']
