"""
Urls for feeds app.
"""
from django.urls import path
from feeds.views import FeedCreate, FeedList

app_name = "feeds"
urlpatterns = [
    path("", FeedList.as_view(), name="home"),
    path("create/", FeedCreate.as_view(), name="create"),
]
