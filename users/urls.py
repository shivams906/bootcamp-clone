from django.contrib.auth import views
from django.urls import path
from users.views import Follow, Login, Network, Profile, SignUp, Unfollow

app_name = "users"
urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("<uuid:pk>/", Profile.as_view(), name="profile"),
    path("<uuid:pk>/follow", Follow.as_view(), name="follow"),
    path("<uuid:pk>/unfollow", Unfollow.as_view(), name="unfollow"),
    path("network/<str:filter>/", Network.as_view(), name="network"),
]
