from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('redirect/', views.google_auth_redirect, name='google_auth_redirect'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('refresh_access_token/', views.refresh_access_token, name='refresh_access_token'),
]