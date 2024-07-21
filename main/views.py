from urllib.parse import urlencode
from django.http import JsonResponse, HttpResponseRedirect
from users.models import GoogleCredentials
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app import settings
from tasks.utils import get_user_tasks

scopes = settings.SCOPES

def index(request):
    user = request.user
    
    try:
        email = user.email
    except AttributeError:
        return redirect("auth:log_in")

    if not user.is_authenticated:
        return redirect('main:login')

    return redirect("main:planner")


def login_view(request):
    return render(request, "index.html")


def signup_view(request):
    return render(request, "index.html")
    

def planner_view(request):
    try:
        user = request.user
        creds = user.get_and_refresh_credentials()
        if creds.refresh_token:
            return render(request, "index.html")
        else:
            return render(request, "index.html", status=403)
    
    except Exception as e:
        return render(request, "index.html", status=500)


def tasks_view(request):
    # return render(request, "index.html")
    user = request.user
    tasks = get_user_tasks(user)
    context = {'tasks': tasks}
    return JsonResponse(context)
    return render(request, "tasks/tasks.html", context=context)


def google_callback(request):
    params = request.GET.dict()

    callback_type = request.session['type']
    if callback_type == 'refresh_permissions':
        google_callback_url = reverse("auth:refresh_permissions_callback")
        url_with_params = f"{google_callback_url}?{urlencode(params)}"
        return HttpResponseRedirect(url_with_params)
    
    if callback_type == 'register':
        google_callback_url = reverse("auth:register_callback")
        url_with_params = f"{google_callback_url}?{urlencode(params)}"
        return HttpResponseRedirect(url_with_params)
    
    if callback_type == 'login':
        google_callback_url = reverse("auth:login_callback")
        url_with_params = f"{google_callback_url}?{urlencode(params)}"
        return HttpResponseRedirect(url_with_params)
    
    return redirect(reverse("main:index"))