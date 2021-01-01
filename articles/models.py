"""
Models for articles app.
"""
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from core.models import TimeStampedModel


class Article(TimeStampedModel):
    """
    Class for article model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the absolute url of article.
        """
        return reverse("articles:detail", args=[self.pk])

    def publish(self):
        """
        Adds a publishing date and time to the article.
        """
        self.published_at = timezone.now()
        self.save()

    @property
    def published(self):
        """
        Returns whether article is published or not.
        """
        return self.published_at is not None