from . import views
from django.urls import path

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("planner/", views.planner_view, name='planner'),
    path("tasks/", views.tasks_view, name='task_view'),
    path("google_callback/", views.google_callback, name="google_callback"),
]
