"""
Contains models, managers, etc. common to the whole project.
"""

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Model class adding a time stamp on instances.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True