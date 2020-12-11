"""
Urls for questions app.
"""
from django.urls import path
from .views import AnswerCreate, QuestionCreate, QuestionDetail, QuestionList

app_name = "questions"
urlpatterns = [
    path("", QuestionList.as_view(), name="home"),
    path("create/", QuestionCreate.as_view(), name="create"),
    path("<uuid:pk>/", QuestionDetail.as_view(), name="detail"),
    path("<uuid:pk>/answer", AnswerCreate.as_view(), name="answer"),
]
