"""
Urls for questions app.
"""
from django.urls import path
from .views import (
    AnswerCreate,
    AnswerEdit,
    QuestionCreate,
    QuestionEdit,
    QuestionDetail,
    QuestionList,
)

app_name = "questions"
urlpatterns = [
    path("", QuestionList.as_view(), name="home"),
    path("create/", QuestionCreate.as_view(), name="create"),
    path("<uuid:pk>/edit/", QuestionEdit.as_view(), name="edit"),
    path("<uuid:pk>/", QuestionDetail.as_view(), name="detail"),
    path("<uuid:pk>/answer/", AnswerCreate.as_view(), name="answer"),
    path(
        "<uuid:question_pk>/answers/<uuid:pk>/edit/",
        AnswerEdit.as_view(),
        name="answer_edit",
    ),
]
