from urllib.parse import urlencode
from django.http import JsonResponse, HttpResponseRedirect
from users.models import GoogleCredentials
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app import settings
from utils import get_and_refresh_user_credentials

scopes = settings.SCOPES


def index(request):
    user = request.user

    if not user:
        return redirect('main:signup')

    if not user.is_authenticated:
        return redirect('main:login')
    
    user_creds = get_and_refresh_user_credentials(user)
    print(user_creds)

    return redirect("main:planner")


def login_view(request):
    return render(request, "index.html")


def signup_view(request):
    return render(request, "index.html")
    

def planner(request):
    return render(request, "index.html")


def google_callback(request):
    params = request.GET.dict()

    callback_type = request.session['type']
    if callback_type == 'refresh_permissions':
        google_callback_url = reverse("auth:refresh_permissions_callback")
        url_with_params = f"{google_callback_url}?{urlencode(params)}"
        return HttpResponseRedirect(url_with_params)
    
    if callback_type in ['refresh_permissions', 'login']:
        google_callback_url = reverse("auth:google_oauth")
        url_with_params = f"{google_callback_url}?{urlencode(params)}"
        return HttpResponseRedirect(url_with_params)
    
    return redirect(reverse("main:index"))