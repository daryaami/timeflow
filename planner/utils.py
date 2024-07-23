
import datetime
import pytz
from datetime import date, datetime, timedelta
from googleapiclient.discovery import build

import concurrent.futures
from main.utils import get_event_colors_hex
from users.utils import get_calendar_by_id
from utils import Priority


def get_event_dict(calendar_id, google_event):
    calendar = get_calendar_by_id(calendar_id=calendar_id)
    (bc_hex, fc_hex) = get_event_colors_hex(google_event['colorId']) if 'colorId' in google_event else (calendar.background_color, calendar.foreground_color)
    event_dict = {
        "id": google_event['id'],
        "summary": google_event['summary'],
        "description": google_event['description'] if 'description' in google_event else None,
        "background_color": bc_hex,
        "foreground_color": fc_hex,
        "start": google_event['start'],
        "end": google_event['end'],
        "calendar": calendar.summary,
        "visibility": google_event["visibility"] if 'visibility' in google_event else None,
    }
    return event_dict


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
        events = events_result.get('items', [])
        return [get_event_dict(calendar_id=calendar_id, google_event=event) for event in events]
    
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

def create_event(user, credentials, calendar_id, **event_details):
    """Creates new calendar event
    Args:
        user_credentials: Credentials
        calendar_id: str
        event_detailes: dict   
            {
                user=user,
                credentials=credentials,
                calendar_id=calendar.calendar_id,
                summary=summary,
                start=start_datetime,
                end=end_datetime,
                description=description,
                color_id=color_id,
                timezone=timezone,
                visibility=visibility,
                timeflow_touched=timeflow_touched,
                timeflow_event_type=timeflow_event_type,
                timeflow_event_id=timeflow_event_id,
                timeflow_control_id=timeflow_control_id,
                timeflow_event_priority=timeflow_event_priority,
                source_url=source_url,
                source_title=source_title

                "summary": "Summary",
                "description": "<i>This event was created by <a href=\"[https://app.timeflow.ai/landing/about?name=Darya+Mitryashkina&utm_source=calendar&utm_campaign=calendar-referral&utm_medium=habit-event&utm_term=xtUPe\\](https://app.reclaim.ai/landing/about?name=Darya+Mitryashkina&utm_source=calendar&utm_campaign=calendar-referral&utm_medium=habit-event&utm_term=xtUPe%5C%5C)">Timeflow</a>.</i><p>This Habit is now marked as done in Timeflow. You can reschedule it to later in the day if you didn't do the Habit, or delete the event if you want to skip it for the day.</p>",
                "colorId": "1",
                "start": {
                    "dateTime": "2024-06-24T09:00:00+03:00",
                    "timeZone": "Europe/Moscow"
                },
                "end": {
                    "dateTime": "2024-06-24T10:30:00+03:00",
                    "timeZone": "Europe/Moscow"
                },
                "visibility": "public",
                "extendedProperties": {
                    "private": {
                            "timeflow.event.category": "personal",
                            "timeflow.priority": "high",
                            "timeflow.colorHash": "49",
                            "timeflow.idHash": "67561455",
                            "timeflow.summaryHash": "675614556",
                            "timeflow.descriptionHash": "-2032938786",
                            "timeflow.touched": "true",
                            },
                        "shared": {
                            "timeflow.busy": "true",
                        }
                    },
                    "source": {
                        "url": "https://app.reclaim.ai/habits/2138279",
                        "title": "Timeflow Habit"
                    }
            }
    """
    timezone = pytz.timezone(event_details['timezone'])
    start_time = event_details['start'].astimezone(timezone).isoformat()
    end_time = event_details['end'].astimezone(timezone).isoformat()

    # return start_time

    event_dict = {
        "summary": event_details['summary'],
        "description":  event_details['description'],
        "colorId": event_details['color_id'],
        "start": {
                    "dateTime": start_time,
                    "timeZone": event_details['timezone']
                },
        "end": {
                    "dateTime": end_time,
                    "timeZone": event_details['timezone']
                },
        "extendedProperties": {
            "private": {
                "timeflow_touched": event_details['timeflow_touched'],
                "timeflow_event_type": event_details['timeflow_event_type'],
                "timeflow_event_id":  event_details['timeflow_event_id'],
                "timeflow_control_id":  event_details['timeflow_control_id'],
                "timeflow_event_priority":  event_details['timeflow_event_priority']
            }
        },
        "visibility": event_details["visibility"],
        "source": {
                    "url": event_details['source_url'],
                    "title": event_details['source_title']
                    }
    }
    try:
        calendar_service = build('calendar', 'v3', credentials=credentials)
        event = calendar_service.events().insert(calendarId=calendar_id, body=event_dict).execute()
        return event
    except Exception as e:
        raise ValueError(f"{e}")