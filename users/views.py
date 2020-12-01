"""
Contains views for users app.
"""
from django.urls import reverse
from django.views import generic
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
