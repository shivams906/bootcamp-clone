"""
Views for polls app.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
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
            Question, Choice, fields=("choice_text",), extra=2, can_delete=True
        )
        context_data["formset"] = ChoiceFormSet()
        return context_data

    def post(self, request, *args, **kwargs):
        form = QuestionModelForm(request.POST)
        ChoiceFormSet = inlineformset_factory(
            Question, Choice, fields=("choice_text",), extra=2, can_delete=True
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


@login_required
def vote(request, pk):
    """
    Votes on the poll.
    """
    question = get_object_or_404(Question, pk=pk)
    if request.user in question.voters.all():
        return render(
            request,
            "polls/poll_detail.html",
            {"question": question, "error_message": "You have already voted."},
        )
    try:
        selected_choice = question.choices.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/poll_detail.html",
            {
                "question": question,
                "error_message": "You did not select a choice.",
            },
        )
    else:
        question.vote(choice=selected_choice, user=request.user)
        return redirect(reverse("polls:detail", args=(question.pk,)))
