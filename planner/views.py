from django.http import JsonResponse, HttpResponseRedirect
from users.models import GoogleCredentials
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build

from planner.utils import get_all_events_by_weekday
from app import settings

from datetime import datetime, timedelta, time
import json
from datetime import datetime, timedelta

scopes = settings.SCOPES

def get_events(request):
    user = request.user
    try:
        # Получение пользовательских учетных данных
        user_credentials = user.get_and_refresh_credentials()
        # Получение списка подключенных календарей
        user_calendars = user.get_calendars()
        
        # Получение даты из параметров запроса
        if user_calendars:
            date_param = request.GET.get('date', None)
            events_by_days = get_all_events_by_weekday(user_calendars, user_credentials, date_param)

        return JsonResponse(events_by_days)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def create_event(user_credentials, calendar_id, event_details):
    try:
        calendar_service = build('calendar', 'v3', credentials=user_credentials)
        event = calendar_service.events().insert(calendarId=calendar_id, body=event_details).execute()
        return event
    except Exception as e:
        return e


@login_required
def update_event(user_credentials, calendar_id, event_id, updated_event_details):
    try:
        calendar_service = build('calendar', 'v3', credentials=user_credentials)
        event = calendar_service.events().update(calendarId=calendar_id, eventId=event_id, body=updated_event_details).execute()
        return event
    except Exception as e:
        return e
    

def plan(request):
    habits = [
        {"id": 125635712, "info": {"days": {"Monday": [("11:00", "14:00"), ("17:00", "19:00")], "Thursday": [("13:00", "14:00")], "Friday": [("15:00", "17:00")]}, "periodicity": "weekly", "num_per_period": 3, "min_duration": 30, "max_duration": 60, "ideal_time": "13:00", "priority": 2, "start_date": "2024-06-24", "end_date": None}},
        {"id": 12871374, "info": {"days": {"Monday": [("11:00", "14:00"), ("17:00", "19:00")], "Thursday": [("13:00", "14:00")], "Friday": [("15:00", "17:00")]}, "periodicity": "weekly", "num_per_period": 3, "min_duration": 30, "max_duration": 60, "ideal_time": "13:00", "priority": 2, "start_date": "2024-06-24", "end_date": None}},
        {"id": 45763878, "info": {"days": {"Tuesday": [("08:00", "10:00"), ("14:00", "16:00")], "Thursday": [("14:00", "16:00")], "Friday": [("15:00", "17:00")]}, "periodicity": "weekly", "num_per_period": 2, "min_duration": 45, "max_duration": 90, "ideal_time": "14:00", "priority": 3, "start_date": "2024-06-24", "end_date": None}}
    ]

    tasks = [
        {"id": 1, "days": {"Monday": [("10:00", "12:00")], "Wednesday": [("10:00", "12:00")]}, "min_duration": 30, "max_duration": 90, "total_duration": 120, "start_date": "2024-06-24", "end_date": "2024-06-27", "priority": 1},
        {"id": 2, "days": {"Monday": [("10:00", "11:00")], "Tuesday": [("09:00", "11:00")], "Thursday": [("15:00", "17:00")]}, "min_duration": 60, "max_duration": 120, "total_duration": 180, "start_date": "2024-06-24", "end_date": "2024-06-29", "priority": 2}
    ]

    occupied_times = {
        "2024-06-24": [("14:00", "15:00")],
        "2024-06-25": [("11:00", "12:00"), ("13:00", "17:00")],
        "2024-06-26": [],
        "2024-06-27": [("12:00", "13:00")],
        "2024-06-28": [],
        "2024-06-29": [],
        "2024-06-30": [],
        "2024-07-01": [],
        "2024-07-02": [],
        "2024-07-03": [],
        "2024-07-04": [],
    }

    def parse_time_intervals(day, intervals):
        parsed_intervals = []
        for interval in intervals:
            start_time = datetime.strptime(f"{day} {interval[0]}", "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(f"{day} {interval[1]}", "%Y-%m-%d %H:%M")
            parsed_intervals.append((start_time, end_time))
        return parsed_intervals

    def parse_occupied_times(occupied_times):
        parsed_occupied_times = {}
        for day, intervals in occupied_times.items():
            parsed_occupied_times[day] = parse_time_intervals(day, intervals)
        return parsed_occupied_times

    def check_availability(interval, occupied):
        for occupied_interval in occupied:
            if interval[0] < occupied_interval[1] and interval[1] > occupied_interval[0]:
                return False
        return True

    def add_to_occupied(schedule, occupied_times):
        for item in schedule["habits"] + schedule["tasks"]:
            start_time = datetime.fromisoformat(item["start"])
            end_time = datetime.fromisoformat(item["end"])
            day = start_time.strftime("%Y-%m-%d")
            if day not in occupied_times:
                occupied_times[day] = []
            occupied_times[day].append((start_time, end_time))
        return occupied_times

    def schedule_habits_tasks(habits, tasks, occupied_times):
        schedule = {"habits": [], "tasks": []}
        occupied_times = parse_occupied_times(occupied_times)
        end_date = datetime.strptime("2024-09-24", "%Y-%m-%d")

        # Combine habits and tasks and sort by priority
        items = [{"type": "habit", "item": habit} for habit in habits] + [{"type": "task", "item": task} for task in tasks]
        items.sort(key=lambda x: x["item"]["info"]["priority"] if x["type"] == "habit" else x["item"]["priority"])

        for entry in items:
            if entry["type"] == "habit":
                habit = entry["item"]
                id = habit["id"]
                info = habit["info"]
                days = info["days"]
                num_per_period = info["num_per_period"]
                min_duration = info["min_duration"]
                max_duration = info["max_duration"]
                ideal_time = datetime.strptime(info["ideal_time"], "%H:%M").time()
                priority = info["priority"]
                start_date = datetime.strptime(info["start_date"], "%Y-%m-%d")

                current_date = start_date
                while current_date <= end_date:
                    day_name = current_date.strftime("%A")
                    if day_name in days:
                        available_intervals = parse_time_intervals(current_date.strftime("%Y-%m-%d"), days[day_name])
                        for interval in available_intervals:
                            duration = timedelta(minutes=max_duration) if check_availability(interval, occupied_times.get(current_date.strftime("%Y-%m-%d"), [])) else timedelta(minutes=min_duration)
                            if interval[1] - interval[0] >= duration:
                                if check_availability(interval, occupied_times.get(current_date.strftime("%Y-%m-%d"), [])):
                                    start = interval[0]
                                    end = start + duration
                                    schedule["habits"].append({"id": id, "start": start.isoformat(), "end": end.isoformat()})
                                    occupied_times[current_date.strftime("%Y-%m-%d")].append((start, end))
                                    num_per_period -= 1
                                    if num_per_period <= 0:
                                        break
                    current_date += timedelta(days=1)

            elif entry["type"] == "task":
                task = entry["item"]
                id = task["id"]
                days = task["days"]
                min_duration = task["min_duration"]
                max_duration = task["max_duration"]
                total_duration = task["total_duration"]
                priority = task["priority"]
                start_date = datetime.strptime(task["start_date"], "%Y-%m-%d")
                end_date = datetime.strptime(task["end_date"], "%Y-%m-%d")

                current_date = start_date
                while current_date <= end_date and total_duration > 0:
                    day_name = current_date.strftime("%A")
                    if day_name in days:
                        available_intervals = parse_time_intervals(current_date.strftime("%Y-%m-%d"), days[day_name])
                        for interval in available_intervals:
                            duration = timedelta(minutes=min_duration)
                            if interval[1] - interval[0] >= duration:
                                if check_availability(interval, occupied_times.get(current_date.strftime("%Y-%m-%d"), [])):
                                    start = interval[0]
                                    end = start + duration
                                    schedule["tasks"].append({"id": id, "start": start.isoformat(), "end": end.isoformat()})
                                    occupied_times[current_date.strftime("%Y-%m-%d")].append((start, end))
                                    total_duration -= min_duration
                                    if total_duration <= 0:
                                        break
                    current_date += timedelta(days=1)

        return schedule

    schedule = schedule_habits_tasks(habits, tasks, occupied_times)
    print(json.dumps(schedule, indent=4))
    return JsonResponse({})
