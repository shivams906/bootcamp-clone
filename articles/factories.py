"""
Factories for articles app.
"""
import factory
from users.factories import UserFactory
from .models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    """
    Factory for Article model.
    """

    class Meta:
        model = Article

    title = factory.Faker("text")
    text = factory.Faker("text")
    author = factory.SubFactory(UserFactory)
