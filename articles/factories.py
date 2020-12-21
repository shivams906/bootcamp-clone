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

    title = factory.Faker("text", max_nb_chars=255)
    text = factory.Faker("text", max_nb_chars=3000)
    author = factory.SubFactory(UserFactory)
