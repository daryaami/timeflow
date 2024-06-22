from urllib.parse import urlencode
from django.http import JsonResponse, HttpResponseRedirect
from users.models import GoogleCredentials
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from googleapiclient.discovery import build

from utils import get_and_refresh_user_credentials
from main.utils import get_user_calendars, get_all_events_by_weekday
from app import settings

scopes = settings.SCOPES


def index(request):
    # user = request.user

    # event_details = {
    #     'summary': 'Йога',
    #     'location': 'Home',
    #     'description': 'Йога сессия',
    #     'start': {
    #         'dateTime': '2024-06-22T09:00:00-07:00',
    #         'timeZone': user.time_zone,
    #     },
    #     'end': {
    #         'dateTime': '2024-06-22T10:00:00-07:00',
    #         'timeZone': user.time_zone,
    #     },
    #     'recurrence': [
    #         'RRULE:FREQ=WEEKLY;COUNT=10'
    #     ],
    #     'attendees': [
    #         {'email': 'example@example.com'},
    #     ],
    #     'reminders': {
    #         'useDefault': False,
    #         'overrides': [
    #             {'method': 'email', 'minutes': 24 * 60},
    #             {'method': 'popup', 'minutes': 10},
    #         ],
    #     },
    # }


    # return 
    # ////////////
    user = request.user

    if not user.is_authenticated:
        return redirect('main:login')
    
    return redirect("main:planner")


@login_required
def planner(request):
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


def create_event(user_credentials, calendar_id, event_details):
    try:
        calendar_service = build('calendar', 'v3', credentials=user_credentials)
        event = calendar_service.events().insert(calendarId=calendar_id, body=event_details).execute()
        return event
    except Exception as e:
        return e
    

def update_event(user_credentials, calendar_id, event_id, updated_event_details):
    try:
        calendar_service = build('calendar', 'v3', credentials=user_credentials)
        event = calendar_service.events().update(calendarId=calendar_id, eventId=event_id, body=updated_event_details).execute()
        return event
    except Exception as e:
        return e


def login_view(request):
    return render(request, "login.html")
    

def google_callback(request):
    params = request.GET.dict()
    
    if params.get('state'):
        google_callback_url = reverse("auth:google_oauth")
        url_with_params = f"{google_callback_url}?{urlencode(params)}"
        return HttpResponseRedirect(url_with_params)
    
    return redirect("main:login")