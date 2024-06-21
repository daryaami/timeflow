from . import views
from django.urls import path

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("planner/", views.planner, name="planner"),
    path("login/", views.login_view, name="login"),
    path("google_callback/", views.google_callback, name="google_callback"),
]
