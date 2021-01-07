"""
Contains views for users app.
"""
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView, redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic, View
from articles.models import Article
from feeds.models import Feed
from polls.models import Question as Poll
from questions.models import Question, Answer
from users.forms import UserCreationForm
from users.models import User


class SignUp(generic.CreateView):
    """
    View class for signing up a user.
    """

    queryset = User.objects.all()
    form_class = UserCreationForm
    template_name = "users/signup.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("users:login")


class Login(LoginView):
    """
    View class for logging in a user.
    """

    template_name = "users/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class Profile(generic.ListView):
    """
    View class for user profile.
    """

    template_name = "users/profile.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        context_data["user"] = user
        if "category" in self.kwargs:
            context_data["category"] = self.kwargs["category"]
        else:
            context_data["category"] = "feeds"
        return context_data

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        if "category" in self.kwargs:
            category = self.kwargs["category"]
            if category == "feeds" or category == "":
                posts = Feed.objects.filter(author=user)
            elif category == "articles":
                posts = Article.objects.filter(author=user).exclude(published_at=None)
            elif category == "questions":
                posts = Question.objects.filter(author=user)
            elif category == "answers":
                posts = Answer.objects.filter(author=user)
            elif category == "polls":
                posts = Poll.objects.filter(author=user)
            else:
                posts = []
        else:
            posts = Feed.objects.filter(author=user)
        return posts


class Follow(LoginRequiredMixin, View):
    """
    View class for following users.
    """

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        user.follow(request.user)
        return redirect(user)


class Unfollow(LoginRequiredMixin, View):
    """
    View class for unfollowing users.
    """

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        user.unfollow(request.user)
        return redirect(user)


class Network(generic.ListView):
    """
    View class for listing folllowers and followees.
    """

    queryset = User.objects.all()
    template_name = "users/network.html"
    paginate_by = 10
    context_object_name = "users"

    def dispatch(self, request, *args, **kwargs):
        if kwargs["filter"] != "all" and request.user.is_anonymous:
            return redirect_to_login(
                request.get_full_path(),
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        users = User.objects.all()
        if self.kwargs["filter"] == "followers":
            users = users.filter(id__in=self.request.user.followers.all())
        if self.kwargs["filter"] == "followees":
            users = users.filter(id__in=self.request.user.followees.all())
        return users

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["filter"] = self.kwargs["filter"]
        return context_data
