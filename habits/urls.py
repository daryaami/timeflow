from . import views
from django.urls import path

app_name = 'habits'

urlpatterns = [
    path("", views.index, name="index"),
    path("get_habits/", views.get_habits, name="get_habits"),
    path("get_habits/<int:id>", views.get_habit_by_id, name="get_habit_by_id"),
    
]