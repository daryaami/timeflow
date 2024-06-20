from django.shortcuts import render, redirect
from main.utils import get_user_credentials
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from users.models import GoogleCredentials, UserCalendar, CustomUser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app import settings
from google_auth_oauthlib.flow import Flow
from urllib.parse import urlencode

scopes = settings.SCOPES


def index(request):
    params = request.GET.dict()
    
    if params.get('state'):
        google_callback_url = reverse("users:google_callback")
        url_with_params = f"{google_callback_url}?{urlencode(params)}"
        return HttpResponseRedirect(url_with_params)

    return redirect("users:login")

    # code = request.GET.get("code")
    # if code:
    #     return redirect(f"http://127.0.0.1:8000/google_auth/oauth2callback?code={code}")

    auth_token = request.COOKIES.get("auth_token")
    if not auth_token:
        return redirect("/login")

    # request.session['my_data'] = 'Some data'
    return HttpResponseRedirect(reverse("main:planner"))


def login(request):
    return render(request, "login.html")


def planner(request):
    user = request.user

    if not user.is_authenticated:
        return redirect('login_view')
    
    google_credentials = GoogleCredentials.objects.get(user=user)
    credentials = Credentials(
        token=google_credentials.access_token,
        refresh_token=google_credentials.refresh_token,
        token_uri=google_credentials.token_uri,
        client_id=google_credentials.client_id,
        client_secret=google_credentials.client_secret,
        scopes=google_credentials.scopes.split(',')
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    # Обновление сохраненных токенов в базе данных
    google_credentials.access_token = credentials.token
    google_credentials.save()

    # Получение списка подключенных календарей
    user_calendars = UserCalendar.objects.filter(user=user)
    calendar_service = build('calendar', 'v3', credentials=credentials)
    events_by_calendar = {}

    for calendar in user_calendars:
        events = calendar_service.events().list(calendarId=calendar.calendar_id).execute()
        events_by_calendar[calendar.calendar_id] = events.get('items', [])

    return JsonResponse({
        'calendars': [{'id': calendar.calendar_id, 'summary': calendar.summary} for calendar in user_calendars],
        'events': events_by_calendar
    })

    # credentials = get_user_credentials(1)

    # if credentials:
    #     service = build("calendar", "v3", credentials=credentials)

    #     try:
    #         service = build("calendar", "v3", credentials=credentials)
    #         now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
    #         today = datetime.datetime.now()
    #         current_weekday = today.weekday()
    #         start_of_week = today - datetime.timedelta(days=current_weekday)
    #         end_of_week = start_of_week + datetime.timedelta(days=6)

    #         current_week_events_result = (
    #             service.events()
    #             .list(
    #                 calendarId="primary",
    #                 timeMin=start_of_week.isoformat() + "Z",
    #                 timeMax=end_of_week.isoformat() + "Z",
    #                 singleEvents=True,
    #                 orderBy="startTime",
    #             )
    #             .execute()
    #         )
    #         current_week_events = current_week_events_result.get("items", [])

    #         # if not current_week_events:
    #         #     return("No upcoming events found.")

    #         # return current_week_events

    #     except HttpError as error:
    #         return error

    # else:
    #     return redirect("/google_auth")

    # context = {"events": current_week_events}

    # return render(request, "main/planner.html", context)
