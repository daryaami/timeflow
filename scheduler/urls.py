from . import views
from django.urls import path

app_name = "scheduler"

urlpatterns = [
    path("schedule/", views.scheduler, name="schedule"),
    ]