"""
Tests for views defined in articles app.
"""
from faker import Faker
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from articles.factories import ArticleFactory
from articles.models import Article
from articles.views import ArticleCreate, ArticleDetail, ArticleList
from users.factories import UserFactory

fake = Faker()


class ArticleListTestCase(TestCase):
    """
    Test class for ArticleList.
    """

    def test_returns_list_of_articles(self):
        """
        Tests that the view returns list of articles.
        """
        article1 = ArticleFactory()
        article2 = ArticleFactory()
        request = RequestFactory().get("")
        response = ArticleList.as_view()(request)
        self.assertIn("article_list", response.context_data)
        articles = response.context_data["article_list"]
        self.assertIn(article1, articles)
        self.assertIn(article2, articles)


class ArticleCreateTestCase(TestCase):
    """
    Test class for ArticleCreate.
    """

    def test_GET_returns_blank_form(self):
        """
        Tests that GET returns blank form for creating a new article.
        """
        user = UserFactory()
        request = RequestFactory().get("")
        request.user = user
        response = ArticleCreate.as_view()(request)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertFalse(form.is_bound)

    def test_valid_POST_creates_article(self):
        """
        Tests that POSTing valid data creates article.
        """
        user = UserFactory()
        request = RequestFactory().post("", {"title": fake.text(), "text": fake.text()})
        request.user = user
        ArticleCreate.as_view()(request)
        self.assertEqual(Article.objects.count(), 1)

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        """
        Tests that unauthenticated users are redirected to login page.
        """
        request = RequestFactory().get("")
        request.user = AnonymousUser()
        response = ArticleCreate.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)


class ArticleDetailTestCase(TestCase):
    """
    Test class for ArticleDetail.
    """

    def test_returns_article_object(self):
        """
        Tests that view returns article object.
        """
        article = ArticleFactory()
        request = RequestFactory().get("")
        response = ArticleDetail.as_view()(request, pk=article.pk)
        self.assertIn("article", response.context_data)
