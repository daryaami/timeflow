from . import views
from django.urls import path

app_name = 'tasks'

urlpatterns = [
    path("create_task/", views.create_task, name="create_task"),
    path("get_tasks/", views.get_tasks, name="get_tasks"),
    path("get_tasks/<int:id>", views.get_task_by_id, name="get_task_by_id"),
    path("test_task/", views.test_task, name="test_task")
]