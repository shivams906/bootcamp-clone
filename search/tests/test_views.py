"""
Tests for views defined in search app.
"""
from django.test import RequestFactory, TestCase
from articles.factories import ArticleFactory
from feeds.factories import FeedFactory
from questions.factories import QuestionFactory
from search.views import Search


class SearchTestCase(TestCase):
    """
    Test class for Search View.
    """

    def test_no_value_for_search_query_returns_empty_queryset(self):
        """
        Tests that if the query term is not provided an empty
        queryset is returned.
        """
        article = ArticleFactory()
        article.publish()
        request = RequestFactory().get("", {})
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 0)

    def test_empty_search_query_returns_empty_queryset(self):
        """
        Tests that if the query term is empty an empty queryset is returned.
        """
        article = ArticleFactory()
        article.publish()
        request = RequestFactory().get("", {"q": ""})
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 0)

    def test_no_value_for_category_field_returns_results_of_default_category(self):
        """
        Tests that if the category is not provided search uses default category.
        """
        article = ArticleFactory(title="same title")
        article.publish()
        feed = FeedFactory(text="same text")
        request = RequestFactory().get("", {"q": "same"})
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 1)
        self.assertNotIn(article, results)
        self.assertIn(feed, results)

    def test_empty_value_for_category_field_returns_results_of_default_category(self):
        """
        Tests that if the category is empty search uses default category.
        """
        article = ArticleFactory(title="same title")
        article.publish()
        feed = FeedFactory(text="same text")
        request = RequestFactory().get("", {"q": "same", "category": ""})
        response = Search.as_view()(request, category="")
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 1)
        self.assertNotIn(article, results)
        self.assertIn(feed, results)

    def test_valid_search_query_and_category_return_results(self):
        """
        Tests that valid values for search query and category returns results.
        """
        article = ArticleFactory()
        article.publish()
        request = RequestFactory().get("", {"q": article.title[:10]})
        response = Search.as_view()(request, category="articles")
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 1)
        self.assertIn(article, results)

    def test_article_search_returns_only_published_articles(self):
        """
        Tests that if articles are searched only published articles are returned.
        """
        article1 = ArticleFactory(title="same")
        article1.publish()
        article2 = ArticleFactory(title="same")
        request = RequestFactory().get("", {"q": "same"})
        response = Search.as_view()(request, category="articles")
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 1)
        self.assertIn(article1, results)
        self.assertNotIn(article2, results)

    def test_results_are_of_the_requested_category_only(self):
        """
        Tests that results are of the requested category only.
        """
        article = ArticleFactory(title="same")
        article.publish()
        feed = FeedFactory(text="same")
        request = RequestFactory().get("", {"q": "same"})
        response = Search.as_view()(request, category="articles")
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 1)
        self.assertIn(article, results)
        self.assertNotIn(feed, results)