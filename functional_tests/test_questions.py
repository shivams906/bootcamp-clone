"""
Functional tests for questions.
"""
from django.urls import reverse
from questions.models import Question
from .base import FunctionalTest, wait_for


class QuestionTest(FunctionalTest):
    """
    Test class for questions.
    """

    def test_can_create_questions(self):
        """
        Tests that user can create question.
        """
        # Edith logs in and goes to the questions' home page.
        self.login("Edith")
        self.browser.get(self.live_server_url + reverse("questions:home"))

        # She clicks on the link to create a new question.
        create_question = wait_for(
            lambda: self.browser.find_element_by_link_text("Ask a question")
        )
        create_question.click()

        # She enters the details and clicks on submit button.
        question_title_box = wait_for(
            lambda: self.browser.find_element_by_name("title")
        )
        question_description_box = wait_for(
            lambda: self.browser.find_element_by_name("description")
        )
        submit_button = wait_for(lambda: self.browser.find_element_by_name("submit"))

        question_title_box.send_keys("title")
        question_description_box.send_keys("description")
        submit_button.click()

        # She is redirected to the question's detail page.
        question = Question.objects.first()
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + question.get_absolute_url(),
            )
        )
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)
        self.assertIn("description", main_content)

        # She returns to questions' home page and
        self.browser.get(self.live_server_url + reverse("questions:home"))

        # sees her question listed there.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)
