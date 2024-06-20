import os
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login
from django.conf import settings
from users.models import GoogleCredentials, UserCalendar, CustomUser
import requests


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
scopes = ['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/calendar']


def login_view(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=scopes)
    flow.redirect_uri = 'http://127.0.0.1:8000'  # Измените на ваш URL-адрес

    authorization_url, state = flow.authorization_url(
        access_type='offline',
    )

    request.session['state'] = state
    return redirect(authorization_url)


def register(request):
        flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=scopes)
        flow.redirect_uri = 'http://127.0.0.1:8000'  # Измените на ваш URL-адрес

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            prompt='consent',
        )

        request.session['state'] = state
        return redirect(authorization_url)


def google_callback(request):
    state = request.session['state']
    authorization_response = request.get_full_path()

    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=scopes, state=state)
    flow.redirect_uri = 'http://127.0.0.1:8000'  # Измените на ваш URL-адрес

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Использование userinfo endpoint для получения информации о пользователе
    userinfo_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'alt': 'json', 'access_token': credentials.token}
    response = requests.get(userinfo_endpoint, params=params)
    user_info = response.json()

    email = user_info['email']

    # Проверяем наличие пользователя в базе, если такой есть, то отправляем на главную страницу
    try:
        user = CustomUser.objects.get(email=email)
        google_credentials = GoogleCredentials.objects.get(user=user)
        if not google_credentials.refresh_token:
            return redirect('users:register')
        login(request, user)
        return redirect('main:planner')
    except CustomUser.DoesNotExist:
        pass  # Пользователь не найден, продолжаем процесс регистрации

    name = user_info['name']
    image_url = user_info.get('picture', '')

    user, created = CustomUser.objects.get_or_create(email=email, defaults={'name': name, 'image': image_url})

    if created:
        # Задание фиктивного пароля для нового пользователя
        user.set_password(CustomUser.objects.make_random_password())
        user.save()
    
    GoogleCredentials.objects.update_or_create(user=user, defaults={
        'access_token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': ','.join(credentials.scopes)
    })

    calendar_service = build('calendar', 'v3', credentials=credentials)
    calendars = calendar_service.calendarList().list().execute()

    for calendar in calendars['items']:
        UserCalendar.objects.update_or_create(user=user, calendar_id=calendar['id'], defaults={'summary': calendar['summary']})

    login(request, user)

    return redirect('main:planner')