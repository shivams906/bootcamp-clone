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
        feed = Feed(text=self.cleaned_data["text"], author=author)
        if commit:
            feed.save()
        return feed
