"""
Tests for forms defined in feeds app.
"""
from django.test import TestCase
from faker import Faker
from feeds.forms import FeedModelForm
from feeds.models import Feed
from users.factories import UserFactory

fake = Faker()


class FeedModelFormTestCase(TestCase):
    """
    Test class for FeedModelForm.
    """

    def test_valid_data_creates_feed(self):
        """
        Tests whether valid data creates a feed.
        """
        user = UserFactory()
        form = FeedModelForm({"text": fake.text(), "author": user.pk})
        self.assertTrue(form.is_valid())
        feed = form.save()
        self.assertEqual(Feed.objects.count(), 1)
        self.assertEqual(Feed.objects.first(), feed)
