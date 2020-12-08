"""
Tests for forms defined in articles app.
"""
from faker import Faker
from django.test import TestCase
from articles.forms import ArticleModelForm
from articles.models import Article
from users.factories import UserFactory

fake = Faker()


class ArticleModelFormTestCase(TestCase):
    """
    Test class for ArticleModelForm.
    """

    def test_valid_data_creates_article(self):
        """
        Tests that valid data creates article.
        """
        user = UserFactory()
        form = ArticleModelForm(
            {"title": fake.text(max_nb_chars=255), "text": fake.text(max_nb_chars=1500)}
        )
        self.assertTrue(form.is_valid())
        form.save(author=user)
        self.assertEqual(Article.objects.count(), 1)
