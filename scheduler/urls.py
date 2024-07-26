from . import views
from django.urls import path

app_name = "scheduler"

urlpatterns = [
    path("schedule_tasks/", views.schedule_tasks, name="schedule_tasks"),
    ]