"""
Contains tests for models defined in users app
"""
import uuid
from django.db import IntegrityError
from django.test import TestCase
import factory
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
        User.objects.create_user(
            name="test", email="test@test.test", password="test123"
        )
        self.assertEqual(User.objects.count(), 1)

    def test_valid_data_creates_superuser(self):
        """
        Tests whether valid data creates a superuser or not.
        """
        user = User.objects.create_superuser(
            name="test", email="test@test.test", password="test123"
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(user.is_superuser)

    def test_string_representation(self):
        """
        Tests tha string representation of User model
        """
        user = UserFactory.build()
        self.assertEqual(str(user), user.name)

    def test_uuid_is_saved_as_id(self):
        """
        Tests that the primary key used for User model is of UUID class
        """
        user = UserFactory.build()
        self.assertIsInstance(user.pk, uuid.UUID)

    def test_no_two_users_have_same_email(self):
        """
        Tests that no two users can have the same email address.
        """
        UserFactory(email="test@test.test")
        with self.assertRaises(IntegrityError):
            UserFactory(email="test@test.test")

    def test_name_is_required(self):
        """
        Tests that name is required.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                name=None, email="test@test.test", password="test@123"
            )

    def test_email_is_required(self):
        """
        Tests that email is required.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(name="test", email=None, password="test@123")

    def test_create_superuser_raises_error_when_is_superuser_is_false(self):
        """
        Tests that create_superuser raises error if is_superuser is false.
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                name="test", email="test@123", password="test@123", is_superuser=False
            )
