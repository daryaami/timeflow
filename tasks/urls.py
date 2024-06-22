from . import views
from django.urls import path

app_name = 'tasks'

urlpatterns = [
    path("", views.index, name="index"),
    path("get_tasks/", views.get_tasks, name="get_tasks"),
    path("get_tasks/<int:id>", views.get_task_by_id, name="get_task_by_id"),
]