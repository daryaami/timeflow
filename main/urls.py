from . import views
from django.urls import path

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),
    path("planner/", views.planner, name="planner"),
    path("create_event/", views.create_event, name='create_event'),
    # path("delete_event/", views.delete_event, name='delete_event'),
    # path("get_event/", views.get_event, name='get_event'),
    # path("update_event/", views.update_event, name='update_event'),
    path("login/", views.login_view, name="login"),
    path("google_callback/", views.google_callback, name="google_callback"),
]
