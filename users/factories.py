"""
Contains a Factory class for creating user object
"""
import factory
from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating user object
    """

    class Meta:
        model = User
