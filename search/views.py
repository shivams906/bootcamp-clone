"""
Views for search app.
"""
from django.contrib.auth import get_user_model
from django.views import generic
from articles.models import Article
from feeds.models import Feed
from polls.models import Question as Poll
from questions.models import Answer, Question

User = get_user_model()


class Search(generic.ListView):
    """
    View class for search.
    """

    template_name = "search/home.html"
    context_object_name = "results"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if "category" in self.kwargs:
            context_data["category"] = self.kwargs["category"]
        else:
            context_data["category"] = "feeds"
        return context_data

    def get_queryset(self):
        search_query = self.request.GET.get("q")
        if not search_query:
            results = []
        else:
            if "category" in self.kwargs:
                category = self.kwargs["category"]
                if category == "feeds" or category == "":
                    results = Feed.objects.filter(text__icontains=search_query)
                elif category == "articles":
                    results = Article.objects.filter(
                        title__icontains=search_query
                    ).exclude(published_at=None)
                elif category == "questions":
                    results = Question.objects.filter(title__icontains=search_query)
                elif category == "answers":
                    results = Answer.objects.filter(text__icontains=search_query)
                elif category == "polls":
                    results = Poll.objects.filter(question_text__icontains=search_query)
                elif category == "users":
                    results = User.objects.filter(name__icontains=search_query)
                else:
                    results = []
            else:
                results = Feed.objects.filter(text__icontains=search_query)
        return results
