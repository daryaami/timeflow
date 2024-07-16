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
    return render(request, "index.html")


def signup_view(request):
    return render(request, "index.html")
    

def planner(request):
    try:
        user = request.user
        creds = user.get_and_refresh_credentials()
        if creds.refresh_token:
            return render(request, "index.html")
        else:
            return render(request, "index.html", status=500)
    
    except Exception as e:
        return JsonResponse({"error": 'e'})
        # return redirect(reverse("auth:refresh_permissions"))


def tasks_view(request):
    return render(request, "index.html")
    # return render(request, "tasks/templates/tasks.html")


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