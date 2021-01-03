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


class Profile(generic.DetailView):
    """
    View class for user profile.
    """

    queryset = User.objects.all()
    template_name = "users/profile.html"


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
