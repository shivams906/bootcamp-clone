"""
Views for questions app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from questions.forms import AnswerModelForm, QuestionModelForm
from questions.models import Answer, Question


class QuestionList(generic.ListView):
    """
    View class for listing questions.
    """

    queryset = Question.objects.all()
    paginate_by = 10
    context_object_name = "questions"


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


class QuestionEdit(LoginRequiredMixin, generic.UpdateView):
    """
    View class for editing questions.
    """

    queryset = Question.objects.all()
    form_class = QuestionModelForm
    template_name = "questions/question_create.html"


class QuestionDetail(generic.DetailView):
    """
    View class for viewing a single question.
    """

    queryset = Question.objects.all()


class AnswerCreate(LoginRequiredMixin, generic.CreateView):
    """
    View class for creating answers.
    """

    queryset = Answer.objects.all()
    form_class = AnswerModelForm
    template_name = "questions/answer_create.html"

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs["pk"])
        form.save(question=question, author=self.request.user)
        return redirect(question)


class AnswerEdit(LoginRequiredMixin, generic.UpdateView):
    """
    View class for editing answers.
    """

    queryset = Answer.objects.all()
    form_class = AnswerModelForm
    template_name = "questions/answer_create.html"
