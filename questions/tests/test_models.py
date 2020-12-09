"""
Tests for models defined in questions app.
"""
from faker import Faker
from django.test import TestCase
from questions.factories import QuestionFactory
from questions.models import Answer, Question
from users.factories import UserFactory

fake = Faker()


class QuestionModelTestCase(TestCase):
    """
    Test class for Question model.
    """

    def test_valid_data_creates_quesetion(self):
        """
        Tests that valid data creates question.
        """
        user = UserFactory()
        question = Question.objects.create(
            title=fake.text(max_nb_chars=255), description=fake.text(), author=user
        )
        self.assertEqual(Question.objects.count(), 1)
        self.assertEqual(Question.objects.first(), question)


class AnswerModelTestCase(TestCase):
    """
    Test class for Answer model.
    """

    def test_valid_data_creates_answer(self):
        """
        Tests that valid data creates answer.
        """
        user = UserFactory()
        question = QuestionFactory()
        answer = Answer.objects.create(text=fake.text(), question=question, author=user)
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Answer.objects.first(), answer)
