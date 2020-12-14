"""
Tests for forms defined in polls app.
"""
from django.test import TestCase
from polls.forms import QuestionModelForm
from polls.models import Question
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
        form = QuestionModelForm({"question_text": "question"})
        self.assertTrue(form.is_valid())
        form.save(author=user)
        self.assertEqual(Question.objects.count(), 1)
