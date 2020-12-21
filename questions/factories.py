"""
Factories for questions app.
"""
import factory
from questions.models import Answer, Question
from users.factories import UserFactory


class QuestionFactory(factory.django.DjangoModelFactory):
    """
    Factory class for Question model.
    """

    class Meta:
        model = Question

    title = factory.Faker("text", max_nb_chars=255)
    description = factory.Faker("text")
    author = factory.SubFactory(UserFactory)


class AnswerFactory(factory.django.DjangoModelFactory):
    """
    Factory class for Answer model.
    """

    class Meta:
        model = Answer

    text = factory.Faker("text")
    question = factory.SubFactory(QuestionFactory)
    author = factory.SubFactory(UserFactory)
