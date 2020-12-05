"""
Contains functional tests for feeds app.
"""
from .base import FunctionalTest


class FeedTestCase(FunctionalTest):
    """
    Test class for feeds.
    """

    def test_can_create_feed(self):
        """
        Tests that user can create feed.
        """
        # Edith goes to the homepage.
        # She sees an input box.
        # She types some text.
        # She clicks on submit.
        # Her feed appears below the box.
        # She creates another post.
        # This one also appear below the box,
        # but above the previous one.
        self.fail("Finish Me!!!")
