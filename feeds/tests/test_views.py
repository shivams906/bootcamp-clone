"""
Tests for views defined in feeds app.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from faker import Faker
from feeds.factories import FeedFactry
from feeds.forms import FeedModelForm
from feeds.models import Feed
from feeds.views import FeedCreate, FeedList
from users.factories import UserFactory

fake = Faker()


class FeedListTestCase(TestCase):
    """
    Test class for FeedList.
    """

    def test_GET_returns_list_of_feeds(self):
        """
        Tests that GET returns list of feeds.
        """
        feed1 = FeedFactry()
        feed2 = FeedFactry()
        request = RequestFactory().get("")
        response = FeedList.as_view()(request)
        self.assertIn("feed_list", response.context_data)
        feeds = response.context_data["feed_list"]
        self.assertIn(feed1, feeds)
        self.assertIn(feed2, feeds)

    def test_GET_returns_empty_form_in_context(self):
        """
        Tests that on GET view returns an empty form for creating feeds.
        """

        request = RequestFactory().get("")
        response = FeedList.as_view()(request)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertIsInstance(form, FeedModelForm)


class FeedCreateTestCase(TestCase):
    """
    Test class for FeedCreate.
    """

    def test_valid_POST_creates_new_feed(self):
        """
        Tests that POSTing valid data creates new feed object.
        """
        text = fake.text()
        request = RequestFactory().post("", {"text": text})
        user = UserFactory()
        request.user = user
        FeedCreate.as_view()(request)
        self.assertEqual(Feed.objects.count(), 1)
        feed = Feed.objects.first()
        self.assertEqual(feed.text, text)

    def test_only_authenticated_users_can_POST(self):
        """
        Tests that only authenticated users can POST.
        """
        text = fake.text()
        request = RequestFactory().post("", {"text": text})
        request.user = AnonymousUser()
        FeedCreate.as_view()(request)
        self.assertEqual(Feed.objects.count(), 0)

    def test_unauthenticated_users_on_POST_are_redirected_to_login_page(self):
        """
        Tests that unauthenticated users on POST are redirected to login page.
        """
        text = fake.text()
        request = RequestFactory().post("", {"text": text})
        request.user = AnonymousUser()
        response = FeedCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)
