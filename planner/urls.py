from . import views
from django.urls import path

app_name = "planner"

urlpatterns = [
    path("", views.index, name="index"),
    path("create_event/", views.create_event, name="create_event"),
    # path("delete_event/", views.delete_event, name='delete_event'),
    # path("get_event/", views.get_event, name='get_event'),
    # path("update_event/", views.update_event, name='update_event'),
]
