from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _

import uuid


class UserManager(BaseUserManager):
    @transaction.atomic
    def create_user(self, name: str, email: str, password: str, **kwargs):
        user = self.model(
            name=name,
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    @transaction.atomic
    def create_superuser(self, name, email, password, **kwargs):
        user = self.create_user(name, email, password, **kwargs)
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser):
    class Meta:
        app_label = 'app'
        db_table = 'users'
        ordering = ('created_at',)
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        abstract = False

    uuid = models.UUIDField(
        verbose_name=_('Public ID'),
        default=uuid.uuid4,
        editable=False,
        unique=True)

    email = models.EmailField(
        verbose_name=_('Email'),
        unique=True)

    password = models.CharField(
        verbose_name=_('Password'),
        max_length=128)

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=150)

    is_active = models.BooleanField(
        verbose_name=_('Is Active?'),
        default=True)

    is_staff = models.BooleanField(
        verbose_name=_('Is Staff?'),
        default=False)

    created_at = models.DateTimeField(
        verbose_name=_('Created Date'),
        auto_now_add=True,
        null=False,
        blank=False,
        help_text=_('Creation datetime.'))

    updated_at = models.DateTimeField(
        verbose_name=_('Updated Date'),
        auto_now=True,
        null=True,
        blank=False,
        help_text=_('Update datetime.'))

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'User<{}>'.format(self.name)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
