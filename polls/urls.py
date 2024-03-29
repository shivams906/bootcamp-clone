"""
Urls for polls app.
"""
from django.urls import path
from polls.views import PollCreate, PollDetail, PollList, vote

app_name = "polls"
urlpatterns = [
    path("", PollList.as_view(), name="home"),
    path("create/", PollCreate.as_view(), name="create"),
    path("<uuid:pk>/", PollDetail.as_view(), name="detail"),
    path("<uuid:pk>/vote", vote, name="vote"),
]
