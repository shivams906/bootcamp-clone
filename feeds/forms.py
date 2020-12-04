"""
Forms for feeds app.
"""
from django import forms
from feeds.models import Feed


class FeedModelForm(forms.ModelForm):
    """
    Form class for Feed model.
    """

    class Meta:
        model = Feed
        fields = "__all__"
