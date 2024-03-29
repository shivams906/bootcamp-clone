"""
Factories for the models in feeds app.
"""
import factory
from users.factories import UserFactory
from .models import Feed


class FeedFactory(factory.django.DjangoModelFactory):
    """
    Factory for Feed model.
    """

    class Meta:
        model = Feed

    text = factory.Faker("text", max_nb_chars=280)
    author = factory.SubFactory(UserFactory)
