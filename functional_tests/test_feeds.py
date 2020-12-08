"""
Contains functional tests for feeds app.
"""
from .base import fake, FunctionalTest, wait_for


class FeedTestCase(FunctionalTest):
    """
    Test class for feeds.
    """

    def test_can_create_feed(self):
        """
        Tests that user can create feed.
        """
        # Edith goes to the homepage.
        self.browser.get(self.live_server_url)

        # She logs in and returns to homepage.
        self.login("Edith")

        # She sees an input box.
        input_box = wait_for(lambda: self.browser.find_element_by_name("text"))

        # She types some text.
        input_box.send_keys("hello")

        # She clicks on submit.
        submit_button = wait_for(lambda: self.browser.find_element_by_name("submit"))
        submit_button.click()

        # Her feed appears below the box.
        feed_list = wait_for(
            lambda: self.browser.find_element_by_class_name("feed_list")
        )
        self.assertIn("hello", feed_list.text)

        # She creates another post.
        input_box = wait_for(lambda: self.browser.find_element_by_name("text"))
        input_box.send_keys("hello again")
        submit_button = wait_for(lambda: self.browser.find_element_by_name("submit"))
        submit_button.click()

        # This one also appear below the box,
        feed_list = wait_for(
            lambda: self.browser.find_element_by_class_name("feed_list")
        )
        self.assertIn("hello again", feed_list.text)

        # but above the previous one.
        feed_items = feed_list.find_elements_by_class_name("feed_item")
        self.assertIn("hello again", feed_items[0].text)
        self.assertIn("hello", feed_items[1].text)
