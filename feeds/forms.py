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
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Write something..."}
            )
        }

    def save(self, author=None, commit=True):
        if author:
            self.instance.author = author
        if commit:
            self.instance.save()
        return self.instance
