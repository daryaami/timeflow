from urllib.parse import urlencode
from django.http import JsonResponse, HttpResponseRedirect
from users.models import GoogleCredentials
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from utils import get_and_refresh_user_credentials
from main.utils import get_user_calendars, get_all_events_by_weekday, get_calendar_events
from app import settings

scopes = settings.SCOPES


def index(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('main:login')
    
    return redirect("main:planner")


@login_required
def planner(request):
    user = request.user

    if not GoogleCredentials.objects.filter(user=user).exists():
        return redirect('main:register')
    if not user.is_authenticated:
        return redirect('main:login')
    
    user_credentials = get_and_refresh_user_credentials(user)

    # Получение списка подключенных календарей
    user_calendars = get_user_calendars(user)

    # Получение даты из параметров запроса
    

    if user_calendars:
        date_param = request.GET.get('date', None)
        events_by_days = get_all_events_by_weekday(date_param, user_calendars, user_credentials)

    context = {'events': events_by_days if events_by_days else {} }

    return render(request, "main/planner.html", context)


def login_view(request):
    return render(request, "login.html")
    

def google_callback(request):
    params = request.GET.dict()
    
    if params.get('state'):
        google_callback_url = reverse("auth:google_oauth")
        url_with_params = f"{google_callback_url}?{urlencode(params)}"
        return HttpResponseRedirect(url_with_params)
    
    return redirect("main:login")
