"""
Factories for models in polls app.
"""
import factory
from polls.models import Choice, Question
from users.factories import UserFactory


class QuestionFactory(factory.django.DjangoModelFactory):
    """
    Factory class for Question model.
    """

    class Meta:
        model = Question

    text = factory.Faker("text", max_nb_chars=255)
    author = factory.SubFactory(UserFactory)


class ChoiceFactory(factory.django.DjangoModelFactory):
    """
    Factory class for Choice model.
    """

    class Meta:
        model = Choice

    text = factory.Faker("text", max_nb_chars=255)
    question = factory.SubFactory(QuestionFactory)
