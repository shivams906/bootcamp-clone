"""
Contains tests for forms defined in users app.
"""
from django.test import TestCase
from faker import Faker
from users.forms import UserCreationForm
from users.models import User

fake = Faker()


class UserCreationFormTestCase(TestCase):
    """
    Test class for UserCreationForm.
    """

    def test_valid_data_creates_a_user(self):
        """
        Tests whether valid data creates a user or not.
        """
        form = UserCreationForm(
            {"name": fake.name(), "email": fake.email(), "password": fake.password()}
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first(), user)

    def test_password_is_saved_correctly(self):
        """
        Tests that password is saved as hashed not plain text.
        """
        form = UserCreationForm(
            {"name": fake.name(), "email": fake.email(), "password": "test@123"}
        )
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertNotEqual(user.password, "test@123")

    def test_email_validation_works(self):
        """
        Tests that email validaions works.
        """
        form = UserCreationForm(
            {"name": fake.name(), "email": "test", "password": fake.password()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_password_validation_works(self):
        """
        Tests that password validaions works.
        """
        form = UserCreationForm(
            {"name": fake.name(), "email": fake.email(), "password": "test"}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)

    def test_name_is_required(self):
        """
        Tests that form shows errors without a name.
        """
        form = UserCreationForm(
            {"name": "", "email": fake.email(), "password": fake.password()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_email_is_required(self):
        """
        Tests that form shows errors without a email.
        """
        form = UserCreationForm(
            {"name": fake.name(), "email": "", "password": fake.password()}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_password_is_required(self):
        """
        Tests that form shows errors without a password.
        """
        form = UserCreationForm(
            {"name": fake.name(), "email": fake.email(), "password": ""}
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password", form.errors)
