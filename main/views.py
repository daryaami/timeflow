from urllib.parse import urlencode
from django.http import JsonResponse, HttpResponseRedirect
from users.models import GoogleCredentials
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app import settings

scopes = settings.SCOPES


def index(request):
    user = request.user

    if not user:
        return redirect('main:signup')
    
    if not user.is_authenticated:
        return redirect('main:login')
    
    return redirect("main:planner")


def login_view(request):
    # return render(request, "login.html")
    return render(request, "index.html")


def signup_view(request):
    return render(request, "index.html")
    

def planner(request):
    return render(request, "index.html")


def google_callback(request):
    params = request.GET.dict()
    
    if params.get('state'):
        google_callback_url = reverse("auth:google_oauth")
        url_with_params = f"{google_callback_url}?{urlencode(params)}"
        return HttpResponseRedirect(url_with_params)
    
    return redirect(reverse("main:index"))