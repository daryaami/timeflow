from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path("login/", views.login_view, name='login'),
    path("register/", views.register, name='register'),
    path("google_oauth/", views.google_oauth, name='google_oauth'),
]