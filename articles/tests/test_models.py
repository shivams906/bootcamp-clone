"""
Tests for models defined in article app.
"""
import uuid
from faker import Faker
from django.test import TestCase
from articles.factories import ArticleFactory
from articles.models import Article
from users.factories import UserFactory

fake = Faker()


class ArticleModelTestCase(TestCase):
    """
    Test class Article model.
    """

    def test_valid_data_creates_article(self):
        """
        Tests that valid data creates article.
        """
        user = UserFactory()
        Article.objects.create(
            title=fake.text(max_nb_chars=255),
            text=fake.text(max_nb_chars=1500),
            author=user,
        )
        self.assertEqual(Article.objects.count(), 1)

    def test_string_representation(self):
        """
        Tests the string representation of Article.
        """
        article = ArticleFactory()
        self.assertEqual(str(article), article.title)

    def test_get_absoolute_url(self):
        """
        Tests that get_absolute_url returns correct url.
        """
        article = ArticleFactory()
        self.assertEqual(article.get_absolute_url(), f"/articles/{article.pk}/")

    def test_id_is_saved_as_uuid(self):
        """
        Tests that id is saved as uuid.
        """
        article = ArticleFactory()
        self.assertIsInstance(article.id, uuid.UUID)

    def test_articles_are_ordered_from_new_to_old(self):
        """
        Tests that articles are ordered from new to old.
        """
        article1 = ArticleFactory()
        article2 = ArticleFactory()
        articles = Article.objects.all()
        self.assertEqual(article1, articles[1])
        self.assertEqual(article2, articles[0])
