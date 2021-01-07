"""
Views for articles app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, reverse
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from .forms import ArticleModelForm
from .models import Article


class ArticleList(ListView):
    """
    View class for listing articles.
    """

    queryset = Article.objects.exclude(published_at=None)
    paginate_by = 10
    context_object_name = "articles"


class ArticleCreate(LoginRequiredMixin, CreateView):
    """
    View class for creating articles.
    """

    queryset = Article.objects.all()
    form_class = ArticleModelForm
    template_name = "articles/article_create.html"

    def form_valid(self, form):
        article = form.save(author=self.request.user)
        if "publish" in self.request.POST:
            article.publish()
        return redirect(article)


class ArticleEdit(UpdateView):
    """
    View class for editing articles.
    """

    queryset = Article.objects.all()
    form_class = ArticleModelForm
    template_name = "articles/article_create.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse("users:login"))
        if self.get_object().author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        article = form.save(instance=self.get_object())
        if "publish" in self.request.POST:
            article.publish()
        return redirect(article)


class ArticleDetail(DetailView):
    """
    View class for single article.
    """

    queryset = Article.objects.all()


class DraftList(LoginRequiredMixin, ListView):
    """
    View class for logged-in user's drafts.
    """

    paginate_by = 10
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).filter(
            published_at=None
        )
