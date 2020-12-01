"""
Contains tests for views defined in users app.
"""
from django.test import RequestFactory, TestCase
from faker import Faker
from users.factories import UserFactory
from users.forms import UserCreationForm
from users.models import User
from users.views import SignUp, Profile

fake = Faker()


class SignUpTestCase(TestCase):
    """
    Test class for SignUp view.
    """

    def test_GET_returns_unbound_signup_form(self):
        """
        Tests that GET request returns a blank signup form.
        """
        request = RequestFactory().get("")
        response = SignUp.as_view()(request)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertIsInstance(form, UserCreationForm)
        self.assertFalse(form.is_bound)

    def test_valid_POST_creates_user(self):
        """
        Tests that POSTing valid data creates a user.
        """
        request = RequestFactory().post(
            "",
            data={
                "name": fake.name(),
                "email": fake.email(),
                "password": fake.password(),
            },
        )
        SignUp.as_view()(request)
        self.assertEqual(User.objects.count(), 1)

    def test_valid_POST_redirects_to_user_detail(self):
        """
        Tests that POSTing valid data redirects to the newly created user's detail page.
        """
        request = RequestFactory().post(
            "",
            data={
                "name": fake.name(),
                "email": fake.email(),
                "password": fake.password(),
            },
        )
        response = SignUp.as_view()(request)
        user = User.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, user.get_absolute_url())

    def test_invalid_POST_returns_bound_form_with_errors(self):
        """
        Tests that POSTing invalid data returns the bound form with errors.
        """
        request = RequestFactory().post(
            "",
            data={
                "name": fake.name(),
                "email": fake.email(),
                "password": "test",
            },
        )
        response = SignUp.as_view()(request)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertIsInstance(form, UserCreationForm)
        self.assertTrue(form.is_bound)
        self.assertNotEqual(len(form.errors), 0)


class ProfileTestCase(TestCase):
    """
    Test class for Profile View.
    """

    def test_GET_returns_user_object(self):
        """
        Tests that GET returns the user object in as context.
        """
        user = UserFactory()
        request = RequestFactory().get("")
        response = Profile.as_view()(request, pk=user.pk)
        self.assertIn("user", response.context_data)
        self.assertEqual(response.context_data["user"], user)
