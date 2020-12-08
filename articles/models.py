"""
Models for articles app.
"""
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse


class Article(models.Model):
    """
    Class for article model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the absolute url of article.
        """
        return reverse("articles:detail", args=[self.pk])
