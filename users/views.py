"""
Contains views for users app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
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

    def get_success_url(self):
        return reverse("users:login")


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
            return redirect(reverse("users:login"))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        users = User.objects.all()
        if self.kwargs["filter"] == "followers":
            users = users.filter(id__in=self.request.user.followers.all())
        if self.kwargs["filter"] == "followees":
            users = users.filter(id__in=self.request.user.followees.all())
        return users

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data["filter"] = self.kwargs["filter"]
        return context_data
