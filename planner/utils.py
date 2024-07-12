from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
from datetime import date, datetime, timedelta
from googleapiclient.discovery import build

from users.models import GoogleCredentials, UserCalendar
import concurrent.futures
from google.auth.exceptions import RefreshError


def get_calendar_events(user_credentials, calendar_id, start_time, end_time):
    try:
        calendar_service = build('calendar', 'v3', credentials=user_credentials)
        events_result = (
            calendar_service.events()
            .list(
                calendarId=calendar_id,
                timeMin=start_time.isoformat() + 'T00:00:00Z',
                timeMax=end_time.isoformat() + 'T00:00:00Z',
                singleEvents=True,
                orderBy='startTime')
            .execute())
        return events_result.get('items', [])
    
    except Exception as e:
        print(f"Error fetching events: {e}")
        print(f"calendar_id: {calendar_id}, timeMin: {start_time.isoformat() + 'T00:00:00Z'}, timeMax: {end_time.isoformat() + 'T00:00:00Z'}")
        return []


def fetch_calendar_events(user_credentials, calendar_id, start_time, end_time):
    return get_calendar_events(user_credentials, calendar_id, start_time, end_time)


def get_all_user_events(user_calendars, user_credentials, start_date=date.today(), time_interval=timedelta(days=90)):
    all_events = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_calendar_events, user_credentials, calendar.calendar_id, start_date, start_date + time_interval)
            for calendar in user_calendars
        ]
        for future in concurrent.futures.as_completed(futures):
            events = future.result()
            all_events.extend(events)
    return all_events


def get_all_events_by_weekday(user_calendars, user_credentials, date_param=None):
    if date_param:
        calendar_date = datetime.strptime(date_param, "%Y-%m-%d").date()
    else:
        calendar_date = date.today()

    start_of_week = calendar_date - timedelta(days=calendar_date.weekday())
    
    days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    events_by_weekday = {day: {"date": (start_of_week + timedelta(days=i)).strftime("%d.%m.%Y"), "events": []} for i, day in enumerate(days_of_week)}

    all_events = get_all_user_events(user_credentials=user_credentials, user_calendars=user_calendars, start_date=start_of_week, time_interval=timedelta(days=7))

    for event in all_events:
        event_start = event['start'].get('dateTime', event['start'].get('date'))
        event_date = datetime.strptime(event_start[:10], '%Y-%m-%d').date()
        weekday = event_date.weekday()
        day_key = days_of_week[weekday]
        events_by_weekday[day_key]["events"].append(event)
    
    return {"days": events_by_weekday}