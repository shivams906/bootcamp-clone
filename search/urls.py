"""
URLs for search app.
"""
from django.urls import path
from .views import Search

app_name = "search"
urlpatterns = [
    path("", Search.as_view(), name="home"),
    path("<str:category>/", Search.as_view(), name="home"),
]