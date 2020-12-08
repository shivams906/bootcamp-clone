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
        article = Article(
            title=self.cleaned_data["title"],
            text=self.cleaned_data["text"],
            author=author,
        )
        if commit:
            article.save()
        return article
