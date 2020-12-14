"""
Tests for views defined in polls app.
"""
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from polls.factories import QuestionFactory
from polls.models import Question
from polls.views import PollCreate, PollDetail, PollList
from users.factories import UserFactory


class PollListTestCase(TestCase):
    """
    Test class for PollList.
    """

    def test_returns_list_of_polls(self):
        """
        Tests that view returns list of polls.
        """
        question1 = QuestionFactory()
        question2 = QuestionFactory()
        request = RequestFactory().get("")
        response = PollList.as_view()(request)
        self.assertIn("question_list", response.context_data)
        polls = response.context_data["question_list"]
        self.assertIn(question1, polls)
        self.assertIn(question2, polls)


class PollCreateTestCase(TestCase):
    """
    Test class for PollCreate.
    """

    def test_GET_returns_empty_form_and_formset(self):
        """
        Tests that GET returns empty form for question and empty formset for choices.
        """
        user = UserFactory()
        request = RequestFactory().get("")
        request.user = user
        response = PollCreate.as_view()(request)
        self.assertIn("form", response.context_data)
        self.assertIn("formset", response.context_data)

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        """
        Tests that unauthenticated users are redirected to login page.
        """
        request = RequestFactory().get("")
        request.user = AnonymousUser()
        response = PollCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)

    def test_valid_POST_creates_poll(self):
        """
        Tests that POSTing valid data creates a poll with question and choices.
        """
        user = UserFactory()
        request = RequestFactory().post(
            "",
            {
                "question_text": "question",
                "choices-TOTAL_FORMS": "4",
                "choices-INITIAL_FORMS": "0",
                "choices-MAX_NUM_FORMS": "",
                "choices-0-choice_text": "choice 1",
                "choices-1-choice_text": "choice 2",
                "choices-2-choice_text": "choice 3",
                "choices-3-choice_text": "choice 4",
            },
        )
        request.user = user
        PollCreate.as_view()(request)
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.choices.count(), 4)


class PollDetailTestCase(TestCase):
    """
    Test class for PollDetail.
    """

    def test_returns_question_object(self):
        """
        Tests that view returns question object.
        """
        question = QuestionFactory()
        request = RequestFactory().get("")
        response = PollDetail.as_view()(request, pk=question.pk)
        self.assertIn("question", response.context_data)
