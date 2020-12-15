"""
Models for polls app.
"""
import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse


class Question(models.Model):
    """
    Model class for questions.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.CharField(max_length=255)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="polls"
    )
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse("polls:detail", args=[self.pk])

    def vote(self, choice=None, user=None):
        """
        Increments the vote count by 1 and saves the user as a voter.
        """
        if user is not None and choice is not None and user not in self.voters.all():
            choice.votes += 1
            self.voters.add(user)
            self.save()
            choice.save()


class Choice(models.Model):
    """
    Model class for choices.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choice_text = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text
