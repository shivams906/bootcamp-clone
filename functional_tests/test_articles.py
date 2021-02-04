"""
Functional tests for articles.
"""
from faker import Faker
from django.contrib.auth import get_user_model
from django.urls import reverse
from .base import FunctionalTest, wait_for
from articles.factories import ArticleFactory

fake = Faker()
User = get_user_model()


class ArticleTest(FunctionalTest):
    """
    Test class for articles.
    """

    def test_can_create_and_publish_articles(self):
        """
        Tests that user can create and publish article.
        """
        # Edith logs in and goes to the articles home page.
        self.login("Edith")
        self.browser.get(self.live_server_url + reverse("articles:home"))

        # She clicks on the link to create a new article.
        create_aticle = wait_for(
            lambda: self.browser.find_element_by_link_text("Create a new article")
        )
        create_aticle.click()

        # She writes the article and clicks on publish.
        title_box = wait_for(lambda: self.browser.find_element_by_name("title"))
        text_box = wait_for(lambda: self.browser.find_element_by_name("text"))
        submit_button = wait_for(
            lambda: self.browser.find_element_by_css_selector("input[name='publish']")
        )

        title_box.send_keys("title")
        text_box.send_keys("text")
        submit_button.click()

        # She is taken to the article's detail page.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)
        self.assertIn("text", main_content)
        self.assertIn("Published at:", main_content)

        # She goes back to articles home page.
        self.browser.get(self.live_server_url + reverse("articles:home"))

        # Her article's title is shown there.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)

    def test_can_save_articles_as_draft(self):
        """
        Tests that user can save articles as draft for publishing later.
        """
        # Edith logs in and goes to the articles home page.
        self.login("Edith")
        self.browser.get(self.live_server_url + reverse("articles:home"))

        # She clicks on the link to create a new article.
        create_aticle = wait_for(
            lambda: self.browser.find_element_by_link_text("Create a new article")
        )
        create_aticle.click()

        # She writes the article and clicks on save as draft.
        title_box = wait_for(lambda: self.browser.find_element_by_name("title"))
        text_box = wait_for(lambda: self.browser.find_element_by_name("text"))
        submit_button = wait_for(
            lambda: self.browser.find_element_by_css_selector("input[name='draft']")
        )

        title_box.send_keys("title")
        text_box.send_keys("text")
        submit_button.click()

        # She is taken to the article's detail page.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)
        self.assertIn("text", main_content)
        self.assertNotIn("Published at:", main_content)
        self.assertIn("Not published", main_content)

        # She goes back to articles home page.
        self.browser.get(self.live_server_url + reverse("articles:home"))

        # Her article's title is not shown there.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertNotIn("title", main_content)

    def test_can_publish_drafts(self):
        """
        Tests that user can publish saved drafts.
        """
        # Edith logs in and goes to articles home page.
        self.login("Edith")
        self.browser.get(self.live_server_url + reverse("articles:home"))

        edith = User.objects.get(name="Edith")
        article = ArticleFactory(title="title", text="text", author=edith)

        # She clicks on the link to her drafts.
        wait_for(lambda: self.browser.find_element_by_link_text("My drafts")).click()

        # She is taken to her drafts' page.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + reverse("articles:drafts"),
            )
        )

        # She clicks on the first entry.
        draft_list = wait_for(lambda: self.browser.find_element_by_id("article_list"))
        drafts = draft_list.find_elements_by_class_name("article_item")
        drafts[0].find_element_by_tag_name("a").click()

        # She is taken to the article's detail page.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + article.get_absolute_url(),
            )
        )

        # She clicks on the edit link.
        wait_for(lambda: self.browser.find_element_by_link_text("Edit")).click()

        # She is taken to a form for editing the draft.
        title_box = wait_for(lambda: self.browser.find_element_by_name("title"))
        text_box = wait_for(lambda: self.browser.find_element_by_name("text"))
        submit_button = wait_for(
            lambda: self.browser.find_element_by_css_selector("input[name='publish']")
        )

        # She clicks on publish.
        submit_button.click()

        # She is taken to the article's detail page.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + article.get_absolute_url(),
            )
        )
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)
        self.assertIn("text", main_content)
        self.assertIn("Published at:", main_content)
        self.assertNotIn("Not published", main_content)

        # She goes back to articles home page.
        self.browser.get(self.live_server_url + reverse("articles:home"))

        # Her article's title is shown there.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("title", main_content)

        # She goes to her drafts.
        wait_for(lambda: self.browser.find_element_by_link_text("My drafts")).click()

        # Her article's title is not shown there.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + reverse("articles:drafts"),
            )
        )
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertNotIn("title", main_content)

    def test_can_update_published_articles(self):
        """
        Tests that user can update published articles.
        """
        # Edith logs in and goes to her article's page.
        self.login("Edith")
        edith = User.objects.get(name="Edith")
        article = ArticleFactory(
            author=edith, title="initial title", text="initial text"
        )
        article.publish()
        self.browser.get(self.live_server_url + article.get_absolute_url())

        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertIn("initial title", main_content)
        self.assertIn("initial text", main_content)

        # She clicks on edit.
        wait_for(lambda: self.browser.find_element_by_link_text("Edit")).click()

        # She is taken to a form for editing.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + reverse("articles:edit", args=[article.pk]),
            )
        )

        # She changes the the title and text and clicks on update.
        title_box = wait_for(lambda: self.browser.find_element_by_name("title"))
        text_box = wait_for(lambda: self.browser.find_element_by_name("text"))
        submit_button = wait_for(
            lambda: self.browser.find_element_by_css_selector("input[name='update']")
        )

        title_box.clear()
        title_box.send_keys("updated title")
        text_box.clear()
        text_box.send_keys("updated text")
        submit_button.click()

        # She is taken to the article's detail page.
        wait_for(
            lambda: self.assertEqual(
                self.browser.current_url,
                self.live_server_url + article.get_absolute_url(),
            )
        )

        # The title and text is changed now.
        main_content = wait_for(
            lambda: self.browser.find_element_by_tag_name("main")
        ).text
        self.assertNotIn("initial title", main_content)
        self.assertIn("updated title", main_content)
        self.assertNotIn("initial text", main_content)
        self.assertIn("updated text", main_content)
