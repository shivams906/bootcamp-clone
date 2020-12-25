"""
Tests for views defined in search app.
"""
from django.test import RequestFactory, TestCase
from articles.factories import ArticleFactory
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
        request = RequestFactory().get("", {"type": "articles"})
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 0)

    def test_empty_search_query_returns_empty_queryset(self):
        """
        Tests that if the query term is empty an empty queryset is returned.
        """
        article = ArticleFactory()
        request = RequestFactory().get("", {"q": "", "type": "articles"})
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 0)

    def test_no_value_for_category_returns_empty_queryset(self):
        """
        Tests that if the category is not provided an empty
        queryset is returned.
        """
        article = ArticleFactory()
        request = RequestFactory().get("", {"q": article.title[:10]})
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 0)

    def test_empty_category_returns_empty_queryset(self):
        """
        Tests that if the category is empty an empty queryset is returned.
        """
        article = ArticleFactory()
        request = RequestFactory().get("", {"q": article.title[:10], "category": ""})
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 0)

    def test_valid_search_query_and_category_return_results(self):
        """
        Tests that valid values for search query and category returns results.
        """
        article = ArticleFactory()
        request = RequestFactory().get(
            "", {"q": article.title[:10], "category": "articles"}
        )
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertEqual(len(results), 1)
        self.assertIn(article, results)

    def test_different_category_returns_different_results(self):
        """
        Tests that different values of category returns different results.
        """
        article = ArticleFactory(title="same")
        question = QuestionFactory(title="same")

        request = RequestFactory().get("", {"q": "same", "category": "articles"})
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertIn(article, results)
        self.assertNotIn(question, results)

        request = RequestFactory().get("", {"q": "same", "category": "questions"})
        response = Search.as_view()(request)
        self.assertIn("results", response.context_data)
        results = response.context_data["results"]
        self.assertNotIn(article, results)
        self.assertIn(question, results)