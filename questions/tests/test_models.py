"""
Tests for models defined in questions app.
"""
import uuid
from faker import Faker
from django.test import TestCase
from questions.factories import AnswerFactory, QuestionFactory
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

    def test_string_representation(self):
        """
        Tests the string representation of Question.
        """
        question = QuestionFactory()
        self.assertEqual(str(question), question.title)

    def test_get_absolute_url(self):
        """
        Tests that get_absolute_url returns correct url.
        """
        question = QuestionFactory()
        self.assertEqual(question.get_absolute_url(), f"/questions/{question.pk}/")

    def test_id_is_saved_as_uuid(self):
        """
        Tests that id is saved as uuid.
        """
        question = QuestionFactory()
        self.assertIsInstance(question.id, uuid.UUID)


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

    def test_string_representation(self):
        """
        Tests the string representation of Answer.
        """
        answer = AnswerFactory()
        self.assertEqual(str(answer), answer.text[100:])

    def test_id_is_saved_as_uuid(self):
        """
        Tests that id is saved as uuid.
        """
        answer = AnswerFactory()
        self.assertIsInstance(answer.id, uuid.UUID)
