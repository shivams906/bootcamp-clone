"""
Forms for articles app.
"""
from django import forms
from .models import Article


class ArticleModelForm(forms.ModelForm):
    """
    Form class for articles.
    """

    class Meta:
        model = Article
        fields = (
            "title",
            "text",
        )

    def save(self, author=None, commit=True):
        if author:
            self.instance.author = author
        if commit:
            self.instance.save()
        return self.instance
