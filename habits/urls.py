from . import views
from django.urls import path

app_name = 'habits'

urlpatterns = [
    path("", views.index, name="index"),
]