"""
Functional tests for polls.
"""
from django.urls import reverse
from .base import FunctionalTest, wait_for
from polls.models import Question


class PollTest(FunctionalTest):
    """
    Tests for polls.
    """

    def test_can_create_poll(self):
        """
        Tests that user can create polls.
        """
        # Edith logs in and goes to the polls' homepage.
        self.login("Edith")
        self.browser.get(self.live_server_url + reverse("polls:home"))

        # She clicks on the link to create a poll.
        create_poll_link = wait_for(
            lambda: self.browser.find_element_by_link_text("Create a poll")
        )
        create_poll_link.click()

        # She enters a question and four choices.
        question_box = wait_for(
            lambda: self.browser.find_element_by_name("question_text")
        )
        choice_1_box = wait_for(
            lambda: self.browser.find_element_by_name("choices-0-choice_text")
        )
        choice_2_box = wait_for(
            lambda: self.browser.find_element_by_name("choices-1-choice_text")
        )
        choice_3_box = wait_for(
            lambda: self.browser.find_element_by_name("choices-2-choice_text")
        )
        choice_4_box = wait_for(
            lambda: self.browser.find_element_by_name("choices-3-choice_text")
        )

        question_box.send_keys("question")
        choice_1_box.send_keys("choice 1")
        choice_2_box.send_keys("choice 2")
        choice_3_box.send_keys("choice 3")
        choice_4_box.send_keys("choice 4")

        # She submits it.
        submit_button = wait_for(lambda: self.browser.find_element_by_name("submit"))
        submit_button.click()

        # She is now on the poll's detail page.
        poll = Question.objects.first()
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url, self.live_server_url + poll.get_absolute_url()
            )
        )
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("question", main_content)
        self.assertIn("choice 1", main_content)
        self.assertIn("choice 2", main_content)
        self.assertIn("choice 3", main_content)
        self.assertIn("choice 4", main_content)

        # She goes back to the polls' homepage.
        self.browser.get(self.live_server_url + reverse("polls:home"))

        # Her poll also appears on the polls' homepage.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("question", main_content)
