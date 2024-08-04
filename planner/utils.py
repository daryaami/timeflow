
import datetime
import pytz
from datetime import date, datetime, timedelta
from googleapiclient.discovery import build

import concurrent.futures
from main.utils import get_event_colors_hex
from users.utils import get_calendar_by_id
from utils import Priority


# def transform_event_timezone(event):

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
    if "extendedProperties" in google_event:
        ext_properties_private = google_event["extendedProperties"]["private"]
        if "timeflow_touched" in ext_properties_private:
            event_dict["timeflow_touched"] = ext_properties_private["timeflow_touched"],
            if ext_properties_private['timeflow_touched'] == 'true':
                event_dict["timeflow_event_type"] =  ext_properties_private.get("timeflow_event_type")
                event_dict["timeflow_event_id"] =  ext_properties_private.get("timeflow_event_id")
                event_dict["timeflow_event_priority"] =  ext_properties_private.get("timeflow_event_priority")
                event_dict["timeflow_event_status"] =  ext_properties_private.get("timeflow_event_status")

    return event_dict


def get_calendar_events(credentials, calendar_id, start_time, end_time):
    try:
        calendar_service = build('calendar', 'v3', credentials=credentials)
        events_result = (
            calendar_service.events()
            .list(
                calendarId=calendar_id,
                timeMin=start_time.isoformat(),
                timeMax=end_time.isoformat(),
                singleEvents=True,
                orderBy='startTime')
            .execute())
        events = events_result.get('items', [])
        return [get_event_dict(calendar_id=calendar_id, google_event=event) for event in events]
    
    except Exception as e:
        print(f"Error fetching events: {e}")
        print(f"calendar_id: {calendar_id}, timeMin: {start_time.isoformat()}, timeMax: {end_time.isoformat()}")
        return []


def get_all_user_events(user, credentials, start_date=None, time_interval=timedelta(days=90)):
    tz = pytz.timezone(user.time_zone)
    user_calendars = user.get_calendars()

    if start_date is None:
        start_date = datetime.combine(date.today(), datetime.min.time())
    start_of_week_datetime = tz.localize(datetime.combine(start_date, datetime.min.time()))

    all_events = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_calendar_events, credentials, calendar.calendar_id, start_of_week_datetime, start_of_week_datetime + time_interval)
            for calendar in user_calendars
        ]
        for future in concurrent.futures.as_completed(futures):
            events = future.result()
            all_events.extend(events)
    return all_events


def get_all_events_by_weekday(user, credentials, date_param=None):
    tz = pytz.timezone(user.time_zone)
    if date_param:
        calendar_date = datetime.strptime(date_param, "%Y-%m-%d").date()
    else:
        calendar_date = date.today()

    start_of_week = calendar_date - timedelta(days=calendar_date.weekday())

    days_of_week = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    events_by_weekday = {day: {"date": (start_of_week + timedelta(days=i)).strftime('%Y-%m-%d'), "events": []} for i, day in enumerate(days_of_week)}

    all_events = get_all_user_events(user=user, credentials=credentials, start_date=start_of_week, time_interval=timedelta(days=7))

    for event in all_events:
        event_start = event['start'].get('dateTime', event['start'].get('date'))
        if 'dateTime' in event['start']:
            event_date = datetime.fromisoformat(event_start).astimezone(tz).date()
        else:
            event_date = datetime.strptime(event_start, '%Y-%m-%d').date()
        
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
                status=LockState

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
                "timeflow_event_priority":  event_details['timeflow_event_priority'],
                "timeflow_event_status": event_details["timeflow_event_status"]
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
        return get_event_dict(calendar_id=calendar_id, google_event=event)
    except Exception as e:
        raise ValueError(f"{e}")