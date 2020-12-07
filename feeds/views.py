"""
Views for feeds app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import generic
from .forms import FeedModelForm
from .models import Feed


class FeedList(generic.ListView):
    """
    View for listing feeds.
    """

    queryset = Feed.objects.all()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["form"] = FeedModelForm()
        return context_data


class FeedCreate(LoginRequiredMixin, generic.CreateView):
    """
    View for creating feeds.
    """

    queryset = Feed.objects.all()
    form_class = FeedModelForm
    success_url = "/feeds/"

    def form_valid(self, form):
        self.object = form.save(author=self.request.user)
        return HttpResponseRedirect(self.get_success_url())
