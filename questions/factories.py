"""
Factories for questions app.
"""
import factory
from questions.models import Question
from users.factories import UserFactory


class QuestionFactory(factory.django.DjangoModelFactory):
    """
    Factory class for Question model.
    """

    class Meta:
        model = Question

    title = factory.Faker("text")
    description = factory.Faker("text")
    author = factory.SubFactory(UserFactory)
