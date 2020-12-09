"""
Views for questions app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic
from questions.forms import QuestionModelForm
from questions.models import Question


class QuestionList(generic.ListView):
    """
    View class for listing questions.
    """

    queryset = Question.objects.all()


class QuestionCreate(LoginRequiredMixin, generic.CreateView):
    """
    View class for creating questions.
    """

    queryset = Question.objects.all()
    form_class = QuestionModelForm
    template_name = "questions/question_create.html"

    def form_valid(self, form):
        question = form.save(author=self.request.user)
        return redirect(question)


class QuestionDetail(generic.DetailView):
    """
    View class for viewing a single question.
    """

    queryset = Question.objects.all()
