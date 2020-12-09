"""
Tests for forms defined in questions app.
"""
from django.test import TestCase
from questions.forms import AnswerModelForm, QuestionModelForm
from questions.factories import QuestionFactory
from questions.models import Answer, Question
from users.factories import UserFactory


class QuestionModelFormTestCase(TestCase):
    """
    Test class for QuestionModelForm.
    """

    def test_valid_data_creates_question(self):
        """
        Tests that valid data creates question.
        """
        user = UserFactory()
        form = QuestionModelForm({"title": "title", "description": "description"})
        self.assertTrue(form.is_valid())
        form.save(author=user)
        self.assertEqual(Question.objects.count(), 1)


class AnswerModelFormTestCase(TestCase):
    """
    Test class for AnswerModelForm.
    """

    def test_valid_data_creates_answer(self):
        """
        Tests that valid data creates answer.
        """
        user = UserFactory()
        question = QuestionFactory()
        form = AnswerModelForm({"text": "text"})
        self.assertTrue(form.is_valid())
        form.save(question=question, author=user)
        self.assertEqual(Answer.objects.count(), 1)
