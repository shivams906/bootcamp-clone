"""
Forms for questions app.
"""
from django import forms
from questions.models import Answer, Question


class QuestionModelForm(forms.ModelForm):
    """
    Model form class for Question model.
    """

    class Meta:
        model = Question
        fields = ("title", "description")

    def save(self, author=None, commit=True):
        self.instance.author = author
        if commit:
            self.instance.save()
        return self.instance


class AnswerModelForm(forms.ModelForm):
    """
    Model form class for Answer model.
    """

    class Meta:
        model = Answer
        fields = ("text",)

    def save(self, question=None, author=None, commit=True):
        answer = Answer(
            text=self.cleaned_data["text"],
            question=question,
            author=author,
        )
        if commit:
            answer.save()
        return answer
