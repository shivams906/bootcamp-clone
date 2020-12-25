"""
Views for search app.
"""
from django.views import generic
from articles.models import Article
from feeds.models import Feed
from polls.models import Question as Poll
from questions.models import Question


class Search(generic.ListView):
    """
    View class for search.
    """

    template_name = "search/home.html"
    context_object_name = "results"
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get("q")
        category = self.request.GET.get("category")
        if (
            search_query is None
            or search_query == ""
            or category is None
            or category == ""
        ):
            results = []
        else:
            if category == "feeds":
                results = Feed.objects.filter(text__icontains=search_query)
            elif category == "articles":
                results = Article.objects.filter(title__icontains=search_query)
            elif category == "questions":
                results = Question.objects.filter(title__icontains=search_query)
            elif category == "polls":
                results = Poll.objects.filter(question_text__icontains=search_query)
            else:
                results = []
        return results
