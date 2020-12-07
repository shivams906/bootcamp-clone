"""
Models for feeds app.
"""
import uuid
from django.conf import settings
from django.db import models


class Feed(models.Model):
    """
    Class for Feed model.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=280)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feeds"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:20]
