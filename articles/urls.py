from django.urls import path
from .views import ArticleCreate, ArticleDetail, ArticleList

app_name = "articles"
urlpatterns = [
    path("", ArticleList.as_view(), name="home"),
    path("<uuid:pk>/", ArticleDetail.as_view(), name="detail"),
    path("create/", ArticleCreate.as_view(), name="create"),
]
