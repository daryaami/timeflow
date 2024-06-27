from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path("login/", views.log_in, name='log_in'),
    path("register/", views.register, name='register'),
    path("google_oauth/", views.google_oauth, name='google_oauth'),
]