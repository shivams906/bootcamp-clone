"""
Contains tests for models defined in users app
"""
import uuid
from unittest import mock
from django.db import IntegrityError
from django.test import TestCase
from faker import Faker
from users.factories import UserFactory
from users.models import User

fake = Faker()


class UserModelTestCase(TestCase):
    """
    Test class for User model
    """

    def test_valid_data_creates_user(self):
        """
        Tests whether valid data creates a user or not
        """
        User.objects.create_user(
            name=fake.name(), email=fake.email(), password=fake.password()
        )
        self.assertEqual(User.objects.count(), 1)

    def test_valid_data_creates_superuser(self):
        """
        Tests whether valid data creates a superuser or not.
        """
        user = User.objects.create_superuser(
            name=fake.name(), email=fake.email(), password=fake.password()
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
            UserFactory(name=None)

    def test_email_is_required(self):
        """
        Tests that email is required.
        """
        with self.assertRaises(ValueError):
            UserFactory(email=None)

    def test_create_superuser_raises_error_when_is_superuser_is_false(self):
        """
        Tests that create_superuser raises error if is_superuser is false.
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                name="test", email="test@123", password="test@123", is_superuser=False
            )

    def test_create_superuser_raises_error_when_is_staff_is_false(self):
        """
        Tests that create_superuser raises error if is_staff is false.
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                name="test", email="test@123", password="test@123", is_staff=False
            )

    def test_get_full_name_returns_name(self):
        """
        Tests that get_full_name returns name.
        """
        user = UserFactory.build()
        self.assertEqual(user.get_full_name(), user.name)

    def test_get_short_name_returns_name(self):
        """
        Tests that get_short_name returns name.
        """
        user = UserFactory.build()
        self.assertEqual(user.get_short_name(), user.name)

    @mock.patch("users.models.send_mail")
    def test_email_user_works_correctly(self, mock_send_mail):
        """
        Tests that email_user correctly calls send_mail function.
        """
        user = UserFactory.build()
        subject = "test"
        message = "test"
        from_email = "test@test.test"
        user.email_user(subject, message, from_email)
        mock_send_mail.assert_called_with(subject, message, from_email, [user.email])
