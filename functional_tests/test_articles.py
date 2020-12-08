"""
Functional tests for articles.
"""
from faker import Faker
from django.urls import reverse
from .base import FunctionalTest, wait_for

fake = Faker()


class ArticleTest(FunctionalTest):
    """
    Test class for articles.
    """

    def test_can_create_article(self):
        """
        Tests that user can create article.
        """
        # Edith logs in and goes to the articles home page.
        self.login("Edith")
        self.browser.get(self.live_server_url + reverse("articles:home"))

        # She clicks on the link to create a new article.
        create_aticle = wait_for(
            lambda: self.browser.find_element_by_link_text("Create a new article")
        )
        create_aticle.click()

        # She writes the article and click on submit.
        title_box = wait_for(lambda: self.browser.find_element_by_name("title"))
        text_box = wait_for(lambda: self.browser.find_element_by_name("text"))
        submit_button = wait_for(
            lambda: self.browser.find_element_by_css_selector("input[type='submit']")
        )

        title_box.send_keys("title")
        text_box.send_keys("text")
        submit_button.click()

        # She is taken to the article detail page.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)
        self.assertIn("text", main_content)

        # She goes back to articles home page.
        self.browser.get(self.live_server_url + reverse("articles:home"))

        # Her article's title is shown there.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)
