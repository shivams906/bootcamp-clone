"""
Contains tests for views defined in users app.
"""
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from django.urls import reverse
from faker import Faker
from users.factories import UserFactory
from users.forms import UserCreationForm
from users.models import Followership, User
from users.views import Follow, Login, Network, Profile, SignUp, Unfollow

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
        request.user = AnonymousUser()
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
        request.user = AnonymousUser()
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
        request.user = AnonymousUser()
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
        request.user = AnonymousUser()
        response = SignUp.as_view()(request)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertIsInstance(form, UserCreationForm)
        self.assertTrue(form.is_bound)
        self.assertNotEqual(len(form.errors), 0)

    def test_authenticated_users_are_redirected_to_login_redirect_url(self):
        """
        Tests that authenticated users are redirected to login redirect url.
        """
        user = UserFactory()
        request = RequestFactory().get("")
        request.user = user
        response = SignUp.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL)


class LoginTestCase(TestCase):
    """
    Test class for Login view.
    """

    def test_authenticated_users_are_redirected_to_login_redirect_url(self):
        """
        Tests that authenticated users are redirected to login redirect url.
        """
        user = UserFactory()
        request = RequestFactory().get("")
        request.user = user
        response = Login.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, settings.LOGIN_REDIRECT_URL)


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


class NetworkTestCase(TestCase):
    """
    Test class for Network view.
    """

    def test_returns_all_users_if_filter_is_all(self):
        """
        Tests that returns all users if filter is all.
        """
        user1 = UserFactory()
        user2 = UserFactory()
        request = RequestFactory().get("")
        response = Network.as_view()(request, filter="all")
        self.assertIn("user_list", response.context_data)
        users = response.context_data["user_list"]
        self.assertIn(user1, users)
        self.assertIn(user2, users)

    def test_returns_only_followers_if_filter_is_followers(self):
        """
        Tests that returns only the user's followers if filter is followers.
        """
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        user1.follow(user2)
        request = RequestFactory().get("")
        request.user = user1
        response = Network.as_view()(request, filter="followers")
        self.assertIn("user_list", response.context_data)
        users = response.context_data["user_list"]
        self.assertNotIn(user1, users)
        self.assertIn(user2, users)
        self.assertNotIn(user3, users)

    def test_returns_only_followees_if_filter_is_followees(self):
        """
        Tests that returns only the user's followees if filter is followees.
        """
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        user2.follow(user1)
        request = RequestFactory().get("")
        request.user = user1
        response = Network.as_view()(request, filter="followees")
        self.assertIn("user_list", response.context_data)
        users = response.context_data["user_list"]
        self.assertNotIn(user1, users)
        self.assertIn(user2, users)
        self.assertNotIn(user3, users)

    def test_unauthenticated_users_are_redirected_to_login_page_if_filer_is_followers(
        self,
    ):
        """
        Tests that unauthenticated users are redirected to login page if
        filter is followers.
        """
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        user1.follow(user2)
        request = RequestFactory().get("")
        request.user = AnonymousUser()
        response = Network.as_view()(request, filter="followers")
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)

    def test_unauthenticated_users_are_redirected_to_login_page_if_filter_is_followees(
        self,
    ):
        """
        Tests that unauthenticated users are redirected to login page if
        filter is followees.
        """
        user1 = UserFactory()
        user2 = UserFactory()
        user3 = UserFactory()
        user2.follow(user1)
        request = RequestFactory().get("")
        request.user = AnonymousUser()
        response = Network.as_view()(request, filter="followees")
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)

    def test_returns_filter_in_context_data(self):
        """
        Tests that view returns filter in context data.
        """
        request = RequestFactory().get("")
        response = Network.as_view()(request, filter="all")
        self.assertIn("filter", response.context_data)