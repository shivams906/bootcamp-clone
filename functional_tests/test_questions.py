"""
Functional tests for questions.
"""
from django.urls import reverse
from questions.factories import QuestionFactory
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

    def test_user_can_answer_questions(self):
        """
        Tests that user can answer questions.
        """
        question = QuestionFactory(title="title")
        # Edith logs in and goes to the questions' home page.
        self.login("Edith")
        self.browser.get(self.live_server_url + reverse("questions:home"))

        # She sees a question and clicks on it.
        question_link = wait_for(
            lambda: self.browser.find_element_by_link_text(question.title)
        )
        question_link.click()

        # She is taken to the question's page.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + reverse("questions:detail", args=[question.pk]),
            )
        )

        # She clicks on the link to answer the question.
        answer_link = wait_for(
            lambda: self.browser.find_element_by_link_text("Answer it")
        )
        answer_link.click()

        # She enters her answer and submits it.
        wait_for(lambda: self.browser.find_element_by_name("answer_form"))
        answer_box = wait_for(lambda: self.browser.find_element_by_name("text"))
        submit_button = wait_for(lambda: self.browser.find_element_by_name("submit"))

        answer_box.send_keys("answer")
        submit_button.click()

        # Her answer now appears below the question.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + reverse("questions:detail", args=[question.pk]),
            )
        )
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("answer", main_content)
