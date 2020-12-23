"""
Contains tests for views defined in users app.
"""
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from faker import Faker
from users.factories import UserFactory
from users.forms import UserCreationForm
from users.models import Followership, User
from users.views import Follow, SignUp, Profile, Unfollow

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

    def test_valid_POST_redirects_to_login_page(self):
        """
        Tests that POSTing valid data redirects to the login page.
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
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login"))

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


class FollowTestCase(TestCase):
    """
    Test class for Follow view.
    """

    def test_GET_creates_a_followership(self):
        """
        Tests that GET creates a followership between users.
        """
        user = UserFactory()
        anotherUser = UserFactory()
        request = RequestFactory().get("")
        request.user = user
        response = Follow.as_view()(request, pk=anotherUser.pk)
        self.assertIn(user, anotherUser.followers.all())
        self.assertIn(anotherUser, user.followees.all())

    def test_GET_redirects_user_to_profile(self):
        """
        Tests that GET redirects user to profile page.
        """
        user = UserFactory()
        anotherUser = UserFactory()
        request = RequestFactory().get("")
        request.user = user
        response = Follow.as_view()(request, pk=anotherUser.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:profile", args=[anotherUser.pk]))

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        """
        Tests that unauthenticated users are redirected to login page.
        """
        user = UserFactory()
        anotherUser = UserFactory()
        request = RequestFactory().get("")
        request.user = AnonymousUser()
        response = Follow.as_view()(request, pk=anotherUser.pk)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)


class UnfollowTestCase(TestCase):
    """
    Test class for Unfollow view.
    """

    def test_GET_removes_a_followership(self):
        """
        Tests that GET removes a followership between users.
        """
        user = UserFactory()
        anotherUser = UserFactory()
        anotherUser.follow(user)
        request = RequestFactory().get("")
        request.user = user
        response = Unfollow.as_view()(request, pk=anotherUser.pk)
        self.assertNotIn(user, anotherUser.followers.all())
        self.assertNotIn(anotherUser, user.followees.all())

    def test_GET_redirects_user_to_profile(self):
        """
        Tests that GET redirects user to profile page.
        """
        user = UserFactory()
        anotherUser = UserFactory()
        anotherUser.follow(user)
        request = RequestFactory().get("")
        request.user = user
        response = Unfollow.as_view()(request, pk=anotherUser.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:profile", args=[anotherUser.pk]))

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        """
        Tests that unauthenticated users are redirected to login page.
        """
        user = UserFactory()
        request = RequestFactory().get("")
        request.user = AnonymousUser()
        response = Follow.as_view()(request, pk=user.pk)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)