from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, first_name=None):

        if username is None:
            raise TypeError("Please Make a Username")
        if email is None:
            raise TypeError("Enter an email address")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,

            is_staff=False,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError("Super Users need a password")
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(db_index=True, max_length=20, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    is_staff = models.BooleanField(default=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):

        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)
        return token
