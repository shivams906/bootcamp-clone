"""
Views for polls app.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.views import generic
from polls.forms import QuestionModelForm
from polls.models import Choice, Question


class PollList(generic.ListView):
    """
    View class for listing polls.
    """

    queryset = Question.objects.all()
    template_name = "polls/poll_list.html"


class PollCreate(LoginRequiredMixin, generic.CreateView):
    """
    View class for creating a poll.
    """

    queryset = Question.objects.all()
    form_class = QuestionModelForm
    template_name = "polls/poll_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        ChoiceFormSet = inlineformset_factory(
            Question, Choice, fields=("choice_text",), extra=4, can_delete=False
        )
        context_data["formset"] = ChoiceFormSet()
        return context_data

    def post(self, request, *args, **kwargs):
        form = QuestionModelForm(request.POST)
        ChoiceFormSet = inlineformset_factory(
            Question, Choice, fields=("choice_text",), extra=4, can_delete=False
        )
        if form.is_valid():
            question = form.save(author=request.user, commit=False)
            formset = ChoiceFormSet(request.POST, instance=question)
            if formset.is_valid():
                question.save()
                formset.save()
                return redirect(question)
        else:
            formset = ChoiceFormSet(request.POST)

        return render(
            request, "polls/poll_create.html", {"form": form, "formset": formset}
        )


class PollDetail(generic.DetailView):
    """
    View class for viewing single poll.
    """

    queryset = Question.objects.all()
    template_name = "polls/poll_detail.html"
