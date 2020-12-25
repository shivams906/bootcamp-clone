"""
Tests for models defined in polls app.
"""
import uuid
from django.test import TestCase
from django.urls import reverse
from polls.factories import ChoiceFactory, QuestionFactory
from polls.models import Choice, Question
from users.factories import UserFactory


class QuestionModelTestCase(TestCase):
    """
    Test class for Question model.
    """

    def test_valid_data_creates_question(self):
        """
        Tests that valid data creates question.
        """
        user = UserFactory()
        Question.objects.create(question_text="question", author=user)
        self.assertEqual(Question.objects.count(), 1)

    def test_string_representation(self):
        """
        Tests the string representation of question.
        """
        question = QuestionFactory()
        self.assertEqual(str(question), question.question_text)

    def test_id_is_saved_as_uuid(self):
        """
        Tests that id is saved as uuid.
        """
        question = QuestionFactory()
        self.assertIsInstance(question.id, uuid.UUID)

    def test_get_absolute_url(self):
        """
        Tests that get_absolute_url returns correct url.
        """
        question = QuestionFactory()
        self.assertEqual(
            question.get_absolute_url(), reverse("polls:detail", args=[question.pk])
        )

    def test_voting_saves_user(self):
        """
        Tests that voting saves the user who voted.
        """
        user = UserFactory()
        question = QuestionFactory()
        choice = ChoiceFactory(question=question)
        question.vote(choice=choice, user=user)
        self.assertIn(user, question.voters.all())
        self.assertEqual(choice.votes, 1)

    def test_a_choice_can_only_be_voted_on_once(self):
        """
        Tests that a user can vote on a choice only once.
        """
        user = UserFactory()
        question = QuestionFactory()
        choice = ChoiceFactory(question=question)
        question.vote(choice=choice, user=user)
        question.vote(choice=choice, user=user)
        self.assertEqual(choice.votes, 1)

    def test_user_can_vote_on_only_one_choice(self):
        """
        Tests that a user can vote on only one choice.
        """
        user = UserFactory()
        question = QuestionFactory()
        choice1 = ChoiceFactory(question=question)
        choice2 = ChoiceFactory(question=question)
        question.vote(choice=choice1, user=user)
        question.vote(choice=choice2, user=user)
        self.assertEqual(choice1.votes, 1)
        self.assertEqual(choice2.votes, 0)

    def test_questions_are_ordered_from_new_to_old(self):
        """
        Tests that questions are ordered from new to old.
        """
        question1 = QuestionFactory()
        question2 = QuestionFactory()
        questions = Question.objects.all()
        self.assertEqual(question1, questions[1])
        self.assertEqual(question2, questions[0])


class ChoiceModelTestCase(TestCase):
    """
    Test class for Choice model.
    """

    def test_valid_data_creates_choice(self):
        """
        Tests that valid data creates choice.
        """
        question = QuestionFactory()
        Choice.objects.create(choice_text="choice", question=question)
        self.assertEqual(Choice.objects.count(), 1)

    def test_string_representation(self):
        """
        Tests the string representation of choice.
        """
        choice = ChoiceFactory()
        self.assertEqual(str(choice), choice.choice_text)

    def test_id_is_saved_as_uuid(self):
        """
        Tests that id is saved as uuid.
        """
        choice = ChoiceFactory()
        self.assertIsInstance(choice.id, uuid.UUID)

    def test_question_can_access_choices(self):
        """
        Tests that question can access choices.
        """
        question = QuestionFactory()
        choice = ChoiceFactory(question=question)
        self.assertEqual(question.choices.count(), 1)
        self.assertIn(choice, question.choices.all())
