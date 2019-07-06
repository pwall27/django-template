import pytest
from faker import Faker

from mixer.backend.django import mixer

from app.models import User

pytestmark = pytest.mark.django_db  # This is put here so that we can save to the database otherwise it will fail because tests are not written to the database.


class TestUser:

    def test_create_instance(self):
        obj = mixer.blend('app.User')
        assert obj.pk is not None, 'Should create a User instance'

    def test_string(self):
        obj = mixer.blend('app.User')
        assert str(obj) == obj.name, 'User string should be its name'

    def test_representation(self):
        obj = mixer.blend('app.User')
        assert repr(obj) == 'User<{}>'.format(obj.name), 'User representation should be its class name with title'

    def test_has_perm(self):
        obj = mixer.blend('app.User')
        assert obj.has_perm(None) == obj.is_staff, 'User has_perm should be equal to is_staff'

    def test_has_module_perms(self):
        obj = mixer.blend('app.User')
        assert obj.has_module_perms(None) == obj.is_staff, 'User has_module_perms should be equal to is_staff'

    def test_create_user(self):
        fake = Faker()
        name = fake.name()
        email = fake.email()
        password = fake.password(length=10, special_chars=True, digits=True,
                                 upper_case=True, lower_case=True)
        user = User.objects.create_user(
            name=name,
            email=email,
            password=password)

        assert user.name == name, f'User name should be {name}'
        assert user.email == email, f'User email should be {email}'
        assert user.password is not None, f'User password should not be None'
        assert user.password != password, f'User password should be different from raw password'
        assert user.check_password(password), f'User password should be encoded'

    def test_create_superuser(self):
        fake = Faker()
        name = fake.name()
        email = fake.email()
        password = fake.password(length=10, special_chars=True, digits=True,
                                 upper_case=True, lower_case=True)
        user = User.objects.create_superuser(
            name=name,
            email=email,
            password=password)

        assert user.is_staff, 'Super user should be a staff'
