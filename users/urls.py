from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('profile/', views.profile, name='profile')
    # path("logout/", views.logout, name='logout')
    path('login/', views.login_view, name='login'),
    path('google_callback/', views.google_callback, name='google_callback'),
    path('register/', views.register, name='register')
]