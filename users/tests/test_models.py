"""
Contains tests for models defined in users app
"""
import uuid
from django.test import TestCase
from users.factories import UserFactory
from users.models import User


class UserModelTestCase(TestCase):
    """
    Test class for User model
    """

    def test_valid_data_creates_user(self):
        """
        Tests whether valid data creates a user or not
        """
        User.objects.create_user(username="test", password="test@123")
        self.assertEqual(User.objects.count(), 1)

    def test_string_representation(self):
        """
        Tests tha string representation of User model
        """
        user = UserFactory(username="test")
        self.assertEqual(str(user), user.username)

    def test_uuid_is_saved_as_id(self):
        """
        Tests that the primary key used for User model is of UUID class
        """
        user = UserFactory()
        self.assertIsInstance(user.pk, uuid.UUID)
