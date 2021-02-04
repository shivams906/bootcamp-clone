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
        if author:
            self.instance.author = author
        if commit:
            self.instance.save()
        return self.instance
