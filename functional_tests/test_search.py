"""
Functional tests for search.
"""
from selenium.webdriver.support.ui import Select
from django.urls import reverse
from .base import FunctionalTest, wait_for
from articles.factories import ArticleFactory


class SearchTestCase(FunctionalTest):
    """
    Test class for search.
    """

    def test_can_search(self):
        """
        Tests that user can perform a successful search.
        """
        # Edith logs in and goes to search's home page.
        self.login("Edith")
        self.browser.get(self.live_server_url + reverse("search:home"))

        # She sees an input box to enter search query.
        search_form = wait_for(lambda: self.browser.find_element_by_name("search_form"))
        input_box = search_form.find_element_by_name("q")

        # She sees a select box to select the category to search.
        select_box = Select(search_form.find_element_by_name("category"))

        # She also sees a submit button.
        submit_button = search_form.find_element_by_css_selector("input[type='submit']")

        # She types in her query and select the articles category
        article = ArticleFactory()
        input_box.send_keys(article.title[:10])
        select_box.select_by_value("articles")

        # and submits it.
        submit_button.click()

        # The results are shown below the input box.
        result_list = wait_for(lambda: self.browser.find_element_by_id("result_list"))

        # She clicks on the first result.
        results = result_list.find_elements_by_id("result_item")
        results[0].find_element_by_tag_name("a").click()

        # She is on the article's detail page.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + article.get_absolute_url(),
            )
        )
