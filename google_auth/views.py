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


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
scopes = settings.SCOPES


def login_view(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=scopes)
    flow.redirect_uri = settings.REDIRECT_URI

    authorization_url, state = flow.authorization_url(
        access_type='offline',
    )

    request.session['state'] = state
    return redirect(authorization_url)


def register(request):
        flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=scopes)
        flow.redirect_uri = settings.REDIRECT_URI

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            prompt='consent',
        )

        request.session['state'] = state
        return redirect(authorization_url)


def google_oauth(request):
    state = request.session['state']
    authorization_response = request.get_full_path()

    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=scopes, state=state)
    flow.redirect_uri = settings.REDIRECT_URI

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Использование userinfo endpoint для получения информации о пользователе
    userinfo_endpoint = settings.USERINFO_ENDPOINT
    params = {'alt': 'json', 'access_token': credentials.token}
    response = requests.get(userinfo_endpoint, params=params)
    user_info = response.json()

    email = user_info['email']

    try:
        user = CustomUser.objects.get(email=email)
        user_credentials = GoogleCredentials.objects.filter(user=user).first()

        if user_credentials and user_credentials.refresh_token:

            if user_credentials.access_token_expiry and user_credentials.access_token_expiry > timezone.now():
                # Access token is still valid, log in the user and redirect to planner
                login(request, user)
                return redirect('main:planner')
            
            else:
                # Refresh the access token
                refresh_request = requests.post(
                    settings.TOKEN_URI,
                    data={
                        'client_id': user_credentials.client_id,
                        'client_secret': user_credentials.client_secret,
                        'refresh_token': user_credentials.refresh_token,
                        'grant_type': 'refresh_token',
                    },
                )
                new_credentials = refresh_request.json()
                user_credentials.access_token = new_credentials['access_token']
                user_credentials.access_token_expiry = timezone.now() + timedelta(seconds=new_credentials['expires_in'])
                user_credentials.save()

                # Log in the user and redirect to planner
                login(request, user)
                return redirect('main:planner')

    except CustomUser.DoesNotExist:
        name = user_info['name']
        image_url = user_info.get('picture', '')

        user, created = CustomUser.objects.get_or_create(email=email, defaults={'name': name, 'image': image_url})

        if created:
            user.set_password(CustomUser.objects.make_random_password())
            user.save()

    GoogleCredentials.objects.update_or_create(user=user, defaults={
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token or user_credentials.refresh_token if user_credentials else credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': ','.join(credentials.scopes),
        'access_token_expiry': timezone.now() + timedelta(seconds=credentials.expiry)
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