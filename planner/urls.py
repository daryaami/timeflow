from . import views
from django.urls import path

app_name = "planner"

urlpatterns = [
    path("get_events/", views.get_events, name="het_events"),
]
