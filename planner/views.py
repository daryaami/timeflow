from django.http import JsonResponse, HttpResponseRedirect
from users.models import GoogleCredentials
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build

from utils import get_and_refresh_user_credentials
from planner.utils import get_user_calendars, get_all_events_by_weekday
from app import settings

scopes = settings.SCOPES

# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")

@login_required
def get_events(request):
    user = request.user

    if not GoogleCredentials.objects.filter(user=user).exists():
        return redirect('auth:register')

    user_credentials = get_and_refresh_user_credentials(user)

    # Получение списка подключенных календарей
    user_calendars = get_user_calendars(user)

    # Получение даты из параметров запроса
    if user_calendars:
        date_param = request.GET.get('date', None)
        events_by_days = get_all_events_by_weekday(date_param, user_calendars, user_credentials)

    context = {'events': events_by_days if events_by_days else {} }

    return render(request, "main/planner.html", context)


@login_required
def create_event(user_credentials, calendar_id, event_details):
    try:
        calendar_service = build('calendar', 'v3', credentials=user_credentials)
        event = calendar_service.events().insert(calendarId=calendar_id, body=event_details).execute()
        return event
    except Exception as e:
        return e
    

@login_required
def update_event(user_credentials, calendar_id, event_id, updated_event_details):
    try:
        calendar_service = build('calendar', 'v3', credentials=user_credentials)
        event = calendar_service.events().update(calendarId=calendar_id, eventId=event_id, body=updated_event_details).execute()
        return event
    except Exception as e:
        return e