"""
Urls for questions app.
"""
from django.urls import path
from .views import QuestionCreate, QuestionDetail, QuestionList

app_name = "questions"
urlpatterns = [
    path("", QuestionList.as_view(), name="home"),
    path("<uuid:pk>/", QuestionDetail.as_view(), name="detail"),
    path("create/", QuestionCreate.as_view(), name="create"),
]
