from django.urls import path
from .views import ArticleCreate, ArticleDetail, ArticleEdit, ArticleList, DraftList

app_name = "articles"
urlpatterns = [
    path("", ArticleList.as_view(), name="home"),
    path("<uuid:pk>/", ArticleDetail.as_view(), name="detail"),
    path("create/", ArticleCreate.as_view(), name="create"),
    path("drafts/", DraftList.as_view(), name="drafts"),
    path("<uuid:pk>/edit/", ArticleEdit.as_view(), name="edit"),
]
