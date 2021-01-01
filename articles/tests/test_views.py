"""
Tests for views defined in articles app.
"""
from faker import Faker
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from django.urls import reverse
from articles.factories import ArticleFactory
from articles.models import Article
from articles.views import (
    ArticleCreate,
    ArticleDetail,
    ArticleEdit,
    ArticleList,
    DraftList,
)
from users.factories import UserFactory

fake = Faker()


class ArticleListTestCase(TestCase):
    """
    Test class for ArticleList.
    """

    def test_returns_list_of_published_articles_only(self):
        """
        Tests that the view returns list of published articles only.
        """
        article1 = ArticleFactory()
        article1.publish()
        article2 = ArticleFactory()
        request = RequestFactory().get("")
        response = ArticleList.as_view()(request)
        self.assertIn("article_list", response.context_data)
        articles = response.context_data["article_list"]
        self.assertIn(article1, articles)
        self.assertNotIn(article2, articles)


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

    def test_article_is_published_if_publish_is_requested(self):
        """
        Tests that the article is published if publish is requested.
        """
        user = UserFactory()
        requset = RequestFactory().post(
            "",
            {
                "title": fake.text(max_nb_chars=255),
                "text": fake.text(),
                "publish": "Publish",
            },
        )
        requset.user = user
        response = ArticleCreate.as_view()(requset)
        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.first()
        self.assertTrue(article.published)

    def test_article_not_published_if_publish_is_not_requested(self):
        """
        Tests that article is not published if publish is not requested.
        """
        user = UserFactory()
        requset = RequestFactory().post(
            "",
            {
                "title": fake.text(max_nb_chars=255),
                "text": fake.text(),
            },
        )
        requset.user = user
        response = ArticleCreate.as_view()(requset)
        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.first()
        self.assertFalse(article.published)


class ArticleEditTestCase(TestCase):
    """
    Test class for ArticleEdit.
    """

    def test_GET_returns_blank_form_with_instance(self):
        """
        Tests that GET returns blank form with an instance.
        """
        article = ArticleFactory()
        request = RequestFactory().get("")
        request.user = article.author
        response = ArticleEdit.as_view()(request, pk=article.pk)
        self.assertIn("form", response.context_data)
        form = response.context_data["form"]
        self.assertFalse(form.is_bound)
        self.assertEqual(form.instance, article)

    def test_valid_POST_updates_article(self):
        """
        Tests that POSTing valid data updates article.
        """
        article = ArticleFactory(title="title")
        request = RequestFactory().post(
            "", {"title": "different title", "text": fake.text()}
        )
        request.user = article.author
        ArticleEdit.as_view()(request, pk=article.pk)
        article.refresh_from_db()
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(article.title, "different title")

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        """
        Tests that unauthenticated users are redirected to login page.
        """
        article = ArticleFactory()
        request = RequestFactory().get("")
        request.user = AnonymousUser()
        response = ArticleEdit.as_view()(request, pk=article.pk)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)

    def test_users_other_than_author_can_not_edit(self):
        """
        Tests that users other than the author can not edit.
        """
        user = UserFactory()
        article = ArticleFactory()
        request = RequestFactory().get("")
        request.user = user
        with self.assertRaises(PermissionDenied):
            ArticleEdit.as_view()(request, pk=article.pk)

    def test_article_is_published_if_publish_is_requested(self):
        """
        Tests that the article is published if publish is requested.
        """
        user = UserFactory()
        article = ArticleFactory()
        requset = RequestFactory().post(
            "",
            {
                "title": article.title,
                "text": article.text,
                "publish": "Publish",
            },
        )
        requset.user = article.author
        response = ArticleEdit.as_view()(requset, pk=article.pk)
        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.first()
        self.assertTrue(article.published)

    def test_article_not_published_if_publish_is_not_requested(self):
        """
        Tests that article is not published if publish is not requested.
        """
        user = UserFactory()
        article = ArticleFactory()
        requset = RequestFactory().post(
            "",
            {
                "title": article.title,
                "text": article.text,
            },
        )
        requset.user = article.author
        response = ArticleEdit.as_view()(requset, pk=article.pk)
        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.first()
        self.assertFalse(article.published)


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


class DraftListTestCase(TestCase):
    """
    Test class for DraftList.
    """

    def test_returns_draft_of_logged_in_user(self):
        """
        Tests that view returns list of drafts for the current logged-in user.
        """
        article = ArticleFactory()
        requset = RequestFactory().get("")
        requset.user = article.author
        response = DraftList.as_view()(requset)
        self.assertIn("article_list", response.context_data)
        articles = response.context_data["article_list"]
        self.assertIn(article, articles)

    def test_unauthenticated_users_are_redirected_to_login_page(self):
        """
        Tests that unauthenticated users are redirected to login page.
        """
        request = RequestFactory().get("")
        request.user = AnonymousUser()
        response = DraftList.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("users:login"), response.url)
