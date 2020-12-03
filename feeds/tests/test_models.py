"""
Tests for models defined in feeds app.
"""
import uuid
from django.test import TestCase
from feeds.factories import FeedFactry
from feeds.models import Feed
from users.factories import UserFactory


class FeedTestCase(TestCase):
    """
    Tets class for Feed model.
    """

    def test_valid_data_creates_feed(self):
        """
        Tests that valid data creates a feed.
        """
        user = UserFactory()
        Feed.objects.create(text="test", author=user)
        self.assertEqual(Feed.objects.count(), 1)

    def test_id_is_an_instance_of_uuid(self):
        """
        Tests that id is an instance of uuid.
        """
        feed = FeedFactry.build()
        self.assertIsInstance(feed.id, uuid.UUID)

    def test_string_representation(self):
        """
        Tests the string representation of Feed object.
        """
        feed = FeedFactry.build()
        self.assertEqual(str(feed), feed.text[:20])
