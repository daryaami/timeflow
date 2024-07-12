from django.utils import timezone
from datetime import timedelta
import os
import requests
from django.shortcuts import redirect
from django.contrib.auth import login
from django.http import JsonResponse
from app import settings
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from users.models import GoogleCredentials, UserCalendar, CustomUser
# from utils import get_and_refresh_user_credentials


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def _create_flow(state=None):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=settings.SCOPES, state=state)
    flow.redirect_uri = settings.REDIRECT_URI
    return flow


def log_in(request):
    flow = _create_flow()

    authorization_url, state = flow.authorization_url(
        access_type='offline',
    )

    request.session['state'] = state
    request.session['type'] = 'login'
    return redirect(authorization_url)


def register(request):
    flow = flow = _create_flow()

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
    )

    request.session['state'] = state
    request.session['type'] = 'register'
    return redirect(authorization_url)


def refresh_permissions(request):
    flow = _create_flow()

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent',
    )

    request.session['state'] = state
    request.session['type'] = 'refresh_permissions'
    return redirect(authorization_url)


def refresh_permissions_callback(request):
    state = request.session['state']
    authorization_response = request.get_full_path()

    flow = flow = _create_flow(state=state)

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Использование userinfo endpoint для получения информации о пользователе - вынести в функцию
    params = {'alt': 'json', 'access_token': credentials.token}
    response = requests.get(settings.USERINFO_ENDPOINT, params=params)
    user_info = response.json()

    email = user_info['email']

    try:
        user = CustomUser.objects.get(email=email)

        GoogleCredentials.objects.update_or_create(user=user, defaults={
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': ','.join(credentials.scopes),
        'access_token_expiry': credentials.expiry
        })

        user_calendars = UserCalendar.objects.filter(user=user)
        if not user_calendars:
            calendar_service = build('calendar', 'v3', credentials=credentials)
            calendars = calendar_service.calendarList().list().execute()
            
            primary_calendar = next((cal for cal in calendars['items'] if cal.get('primary', False)), None)
            if primary_calendar:
                user_timezone = primary_calendar['timeZone']
                user.time_zone = user_timezone
                user.save()
            
            for calendar in calendars['items']:
                UserCalendar.objects.update_or_create(user=user, calendar_id=calendar['id'], defaults={'summary': calendar['summary']})

        login(request, user)
        return redirect('main:index')

    except Exception as e:
        redirect("auth:register")


def google_oauth(request):
    state = request.session['state']
    authorization_response = request.get_full_path()

    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=settings.SCOPES, state=state)
    flow.redirect_uri = settings.REDIRECT_URI

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Использование userinfo endpoint для получения информации о пользователе - вынести в функцию
    params = {'alt': 'json', 'access_token': credentials.token}
    response = requests.get(settings.USERINFO_ENDPOINT, params=params)
    user_info = response.json()

    email = user_info['email']

    try:
        user = CustomUser.objects.get(email=email)

        user_credentials = user.get_and_refresh_user_credentials()

        if user_credentials:
            # Log in the user and redirect to planner
            login(request, user)
            return redirect('main:planner')
        else:
            redirect("auth:register")

    except CustomUser.DoesNotExist:
        if credentials.refresh_token:
            name = user_info['name']
            image_url = user_info.get('picture', '')

            user, created = CustomUser.objects.get_or_create(email=email, defaults={'name': name, 'image': image_url})

            if created:
                user.set_password(CustomUser.objects.make_random_password())
                user.save()

    if not user and not credentials.refresh_token:
        return redirect("auth:register")

    # Update or create GoogleCredentials
    GoogleCredentials.objects.update_or_create(user=user, defaults={
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': ','.join(credentials.scopes),
        'access_token_expiry': credentials.expiry
    })

    calendar_service = build('calendar', 'v3', credentials=credentials)
    calendars = calendar_service.calendarList().list().execute()
    
    primary_calendar = next((cal for cal in calendars['items'] if cal.get('primary', False)), None)
    if primary_calendar:
        user_timezone = primary_calendar['timeZone']
        user.time_zone = user_timezone
        user.save()
    
    for calendar in calendars['items']:
        UserCalendar.objects.update_or_create(user=user, calendar_id=calendar['id'], defaults={'summary': calendar['summary']})

    login(request, user)
    return redirect('main:planner')