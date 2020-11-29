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

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)
