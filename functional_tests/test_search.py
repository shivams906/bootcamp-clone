"""
Functional tests for search.
"""
from django.urls import reverse
from .base import FunctionalTest, wait_for
from articles.factories import ArticleFactory


class SearchTestCase(FunctionalTest):
    """
    Test class for search.
    """

    def test_user_can_search(self):
        """
        Tests that user can perform a successful search.
        """
        # Edith goes to the search page.
        self.browser.get(self.live_server_url + reverse("search:home"))

        # She sees text instructing her to enter a search term.
        main_content = wait_for(lambda: self.browser.find_element_by_tag_name("main"))
        self.assertIn("Enter a search term", main_content.text)

        # She sees an input box to enter search term and a submit button.
        search_form = main_content.find_element_by_name("search_form")
        input_box = search_form.find_element_by_css_selector("input[name='q']")
        submit_button = search_form.find_element_by_css_selector("input[type='submit']")

        article = ArticleFactory(title="title")
        article.publish()

        # She enters a search term and clicks on submit.
        input_box.send_keys("t")
        submit_button.click()

        # The results are displayed below the input box.
        results = wait_for(lambda: self.browser.find_element_by_id("results"))

        # The results are for feeds.
        results_category = results.find_element_by_id("results_category")
        self.assertIn("feeds", results_category.text)

        # She sees a link to go to articles' search results and clicks on it.
        results.find_element_by_link_text("Articles").click()

        # The results for articles are shown.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url
                + f'{reverse("search:home", kwargs={"category": "articles"})}?q=t',
            )
        )
        results = wait_for(lambda: self.browser.find_element_by_id("results"))
        results_category = results.find_element_by_id("results_category")
        self.assertIn("articles", results_category.text)

        # She sees her article in the list and clicks on it.
        result_list = results.find_element_by_id("result_list")
        result_items = result_list.find_elements_by_class_name("result_item")
        result_items[0].find_element_by_tag_name("a").click()

        # She is on her article's detail page.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + article.get_absolute_url(),
            )
        )
