"""
Contains the User model class
"""
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.text import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Manager class for User model.
    """

    def _create_user(self, name, email, password, **extra_fields):
        """
        Create and save a user with given name, email and password.
        """
        if not email:
            raise ValueError(_("Users must have an email address"))

        if not name:
            raise ValueError(_("Users must have a name"))

        email = self.normalize_email(email)
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email, password=None, **extra_fields):
        """
        Create and save a user with given name, email and password.
        """
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, name, email, password=None, **extra_fields):
        """
        Create and save a superuser with given name, email and password.
        """
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(name, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    A class defining the user model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("name"), max_length=255)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.name
