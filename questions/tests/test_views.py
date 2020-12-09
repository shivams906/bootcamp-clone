"""
Tests for views defined in questions app.
"""
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from questions.factories import QuestionFactory
from questions.forms import QuestionModelForm
from questions.models import Question
from questions.views import QuestionCreate, QuestionDetail, QuestionList
from users.factories import UserFactory


class QuestionListTestCase(TestCase):
    """
    Test class for QuestionTest.
    """

    def test_returns_list_of_questions(self):
        """
        Tests that the view returns a list of questions.
        """
        question1 = QuestionFactory()
        question2 = QuestionFactory()
        request = RequestFactory().get("")
        response = QuestionList.as_view()(request)
        self.assertIn("question_list", response.context_data)
        questions = response.context_data["question_list"]
        self.assertIn(question1, questions)
        self.assertIn(question2, questions)


class QuestionCreateTestCase(TestCase):
    """
    Test class for QuestionCreate.
    """

    def test_GET_returns_blank_form(self):
        """
        Tests that GET returns blank form.
        """
        user = UserFactory()
        request = RequestFactory().get("")
        request.user = user
        response = QuestionCreate.as_view()(request)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertIsInstance(form, QuestionModelForm)

    def test_valid_POST_creates_question(self):
        """
        Tests that POSTing valid data creates question.
        """
        user = UserFactory()
        request = RequestFactory().post(
            "", {"title": "title", "description": "description"}
        )
        request.user = user
        QuestionCreate.as_view()(request)
        self.assertEqual(Question.objects.count(), 1)

    def test_valid_POST_redirects_to_the_question_detail_page(self):
        """
        Tests that POSTing valid data redirects user
        to the question's detail page.
        """
        user = UserFactory()
        request = RequestFactory().post(
            "", {"title": "title", "description": "description"}
        )
        request.user = user
        response = QuestionCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        question = Question.objects.first()
        self.assertEqual(response.url, question.get_absolute_url())

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        """
        Tests that unauthenticated users are redirected to login page.
        """
        request = RequestFactory().get("")
        request.user = AnonymousUser()
        response = QuestionCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)


class QuestionDetailTestCase(TestCase):
    """
    Test class for QuestionDetail.
    """

    def test_returns_question_object(self):
        """
        Tests that view returns question object.
        """
        question = QuestionFactory()
        request = RequestFactory().get("")
        response = QuestionDetail.as_view()(request, pk=question.pk)
        self.assertIn("question", response.context_data)
        self.assertEqual(response.context_data["question"], question)
