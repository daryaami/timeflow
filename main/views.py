from django.shortcuts import render, redirect
from main.utils import get_user_credentials
from django.http import JsonResponse, HttpResponse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import datetime
from django.contrib.auth.decorators import login_required


def index(request):
    code = request.GET.get("code")
    if code:
        return redirect(f"http://127.0.0.1:8000/google_auth/oauth2callback?code={code}")

    auth_token = request.COOKIES.get("auth_token")
    if not auth_token:
        return redirect("/login")

    return redirect("/planner")


def login(request):
    return render(request, "login.html")


def planner(request):
    credentials = get_user_credentials(1)

    if credentials:
        service = build("calendar", "v3", credentials=credentials)

        try:
            service = build("calendar", "v3", credentials=credentials)
            now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
            today = datetime.datetime.now()
            current_weekday = today.weekday()
            start_of_week = today - datetime.timedelta(days=current_weekday)
            end_of_week = start_of_week + datetime.timedelta(days=6)

            current_week_events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=start_of_week.isoformat() + "Z",
                    timeMax=end_of_week.isoformat() + "Z",
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            current_week_events = current_week_events_result.get("items", [])

            # if not current_week_events:
            #     return("No upcoming events found.")

            # return current_week_events

        except HttpError as error:
            return error

    else:
        return redirect("/google_auth")

    context = {"events": current_week_events}

    return render(request, "main/planner.html", context)
