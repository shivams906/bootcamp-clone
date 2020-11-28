"""
Contains tests for models defined in users app
"""
from django.test import TestCase
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
