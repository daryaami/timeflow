from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path("login/", views.log_in, name='log_in'),
    path("register/", views.register, name='register'),
    path("refresh_permissions/", views.refresh_permissions, name='refresh_permissions'),
    path("google_oauth/", views.google_oauth, name='google_oauth'),
    path("login_callback/", views.login_callback, name='login_callback'),
    path("register_callback/", views.register_callback, name='register_callback'),
    path("refresh_permissions_callback/", views.refresh_permissions_callback, name='refresh_permissions_callback'),
]