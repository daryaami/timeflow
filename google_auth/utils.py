from app import settings
from google_auth_oauthlib.flow import Flow
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from users.models import CustomUser, UserCalendar
from googleapiclient.discovery import build
from django.db import IntegrityError


def create_flow(state=None):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE, scopes=settings.SCOPES, state=state
    )
    flow.redirect_uri = settings.REDIRECT_URI
    return flow


def get_userinfo_from_endpoint(credentials):
    """Получение информации о пользователе через userinfo endpoint

    Args:
    credentials (google.auth.external_account_authorized_user.Credentials | google.oauth2.credentials.Credentials)

    Returns:
    userinfo json
    """
    try:
        params = {"alt": "json", "access_token": credentials.token}
        response = requests.get(settings.USERINFO_ENDPOINT, params=params)
        return response.json()
    except:
        raise ValueError("Could not get user info from userinfo endpoint.")


def register_new_user(user_info: dict) -> tuple[CustomUser, bool]:
    user, created = CustomUser.objects.get_or_create(
        email=user_info["email"],
        defaults={"name": user_info["name"], "image": user_info.get("picture", "")},
    )

    if created:
        user.set_password(CustomUser.objects.make_random_password())
        user.save()
        return (user, True)
    
    return (user, False)


def set_user_calendars_and_timezone(user, credentials, calendars_choice=None):
    # Добавить выбор календарей
    try:
        calendar_service = build('calendar', 'v3', credentials=credentials)
        calendars = calendar_service.calendarList().list().execute()

        # calendars_to_set = [calendar for calendar in calendars['items'] if calendar["summary"] in calendars_choice]
        calendars_to_set = calendars['items']

        if not user.time_zone:
            primary_calendar = calendar_service.calendars().get(calendarId='primary').execute()
            time_zone = primary_calendar.get('timeZone')

            user.time_zone = time_zone
            user.save()
        
        for calendar in calendars_to_set:
            try:
                new_calendar = UserCalendar.objects.update_or_create(user=user, calendar_id=calendar['id'], defaults={'summary': calendar['summary'], 'primary': calendar.get('primary', False), 'background_color':calendar.get('backgroundColor', None), 'foreground_color':calendar.get('foregroundColor', None)})
                print(calendar)
            except IntegrityError as e:
                print(f"Integrity error at {calendar['summary']} for user with email {user.email}. Calendar with this summary already exists.")
        return True
    except:
        raise ValueError("Could not set user calendars")