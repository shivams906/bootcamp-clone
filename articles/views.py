"""
Views for articles app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, ListView
from .forms import ArticleModelForm
from .models import Article


class ArticleList(ListView):
    """
    View class for listing articles.
    """

    queryset = Article.objects.all()


class ArticleCreate(LoginRequiredMixin, CreateView):
    """
    View class for creating articles.
    """

    queryset = Article.objects.all()
    form_class = ArticleModelForm
    template_name = "articles/article_create.html"

    def form_valid(self, form):
        article = form.save(author=self.request.user)
        return redirect(article)


class ArticleDetail(DetailView):
    """
    View class for single article.
    """

    queryset = Article.objects.all()
