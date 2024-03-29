"""
Models for questions app.
"""
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse
from core.models import TimeStampedModel


class Question(TimeStampedModel):
    """
    Model class for questions.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns absolute url of question.
        """
        return reverse("questions:detail", args=[self.pk])


class Answer(TimeStampedModel):
    """
    Model class for answers.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answers"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:100]

    def get_absolute_url(self):
        """
        Returns absolute url of answer.
        """
        return reverse("questions:detail", args=[self.question.pk])
