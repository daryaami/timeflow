from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # path('profile/', views.profile, name='profile')
    # path("logout/", views.logout, name='logout')
    path("get_user_info/", views.get_user_info, name='get_user_info')
]