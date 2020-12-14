"""
Forms for polls app.
"""
from django import forms
from polls.models import Question


class QuestionModelForm(forms.ModelForm):
    """
    ModelForm for questions.
    """

    class Meta:
        model = Question
        fields = ("question_text",)

    def save(self, author=None, commit=True):
        question = Question(
            question_text=self.cleaned_data["question_text"], author=author
        )
        if commit:
            question.save()
        return question
