from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("planner/", views.planner, name="planner"),
    path("login/", views.login, name="login"),
]
