import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIRequestFactory

from app.models import User
from app.views import APILoginView, APIRefreshView


@pytest.fixture(scope='module')
def factory():
    return APIRequestFactory()


@pytest.fixture(scope='module')
def fake():
    return Faker()


class TestLoginView:
    def test_login(self, db, factory, fake):
        name = fake.name()
        email = fake.email()
        password = fake.password(length=10, special_chars=True, digits=True,
                                 upper_case=True, lower_case=True)
        User.objects.create_user(
            name=name,
            email=email,
            password=password)

        request = factory.post('/auth/login', {
            'email': email,
            'password': password
        })
        response = APILoginView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK, 'Should be possible to login using API.'
        assert response.data['access_token'], 'access_token should be in the request body response'
        assert response.data['refresh_token'], 'refresh_token should be in the request body response'

    def test_login_wrong_credentials(self, db, factory, fake):
        request = factory.post('/auth/login', {
            'email': fake.email(),
            'password': fake.password()
        })
        response = APILoginView.as_view()(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, 'Should not be possible authenticate with wrong credentials'


class TestRefreshView:

    def test_refresh(self, db, factory, fake):
        name = fake.name()
        email = fake.email()
        password = fake.password(length=10, special_chars=True, digits=True,
                                 upper_case=True, lower_case=True)
        User.objects.create_user(
            name=name,
            email=email,
            password=password)

        factory = APIRequestFactory()
        request = factory.post('/auth/login', {
            'email': email,
            'password': password
        })
        response = APILoginView.as_view()(request)

        access_token = response.data['access_token']
        request = factory.post('/auth/refresh', data={})
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + response.data['refresh_token']

        response = APIRefreshView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK, 'Should be possible to refresh token using API.'
        assert response.data['access_token'], 'A new access_token should be in the request body response'
        assert response.data['access_token'] != access_token, 'The new access_token should be different from other'

    def test_refresh_wrong_token(self, db, factory, fake):
        request = factory.post('/auth/refresh', {})
        request.META['HTTP_AUTHORIZATION'] = fake.name()
        response = APIRefreshView.as_view()(request)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, 'Should not be possible refresh with wrong token'
