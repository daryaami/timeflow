from utils import LockState
from .models import Task
from datetime import datetime
import uuid
from planner.utils import create_event


def get_user_tasks_json(user):
    try:
        user_tasks = Task.objects.filter(user=user)
        return [task.to_json() for task in user_tasks]
    except Exception as e:
        raise ValueError(f"Error getting user tasks json: {e}")


def get_user_tasks(user):
    try:
        return Task.objects.filter(user=user)
    except Exception as e:
        raise ValueError(f"Error getting user tasks: {e}")


def create_new_user_task(user, **params):
    try:
        task = Task.objects.create(
            name=params["name"],
            priority=params["priority"],
            duration=params["duration"],
            min_duration=params["min_duration"],
            max_duration=params["max_duration"],
            schedule_after=params["schedule_after"],
            due_date=params["due_date"],
            hours=params["hours"],
            user=user,
            private=params["private"],
            color=params["color"]
        )
        return task
    except Exception as e:
        raise ValueError(f"Failed to create a new task: Exception {e}")


def create_task_event(
    task_model: Task, start_datetime: datetime, end_datetime: datetime, status: LockState
):
    """ 
    Создает событие задачи в календаре.
    Args: 
    task_model: Task, задача
    start_datetime, end_datetime: datetime tzaware, начало и конец события 
    status: LockState, указывает на источник события. Если событие запланировано алгоритмом и еще не прошло - FREE, если пользователем - MANUAL, если событие прошло - PAST
    """
    try:
        user = task_model.user
        credentials = user.get_and_refresh_credentials()
        calendar = task_model.hours.calendar

        color_id = str(task_model.color.color_id) if task_model.color else None
        timeflow_touched = True
        timeflow_event_type = "0"
        timeflow_event_id = str(task_model.pk)
        timeflow_control_id = str(uuid.uuid4())
        timeflow_event_priority = task_model.priority
        timeflow_event_status = status.value
        timezone = user.time_zone
        summary = task_model.name
        description = "<i>This event was created by TimeFlow.</i>"
        visibility = "private" if task_model.private else "public"
        source_url = f"http://127.0.0.1:8000/tasks/{task_model.pk}"
        source_title = "Timeflow Task"

        new_event = create_event(
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
            timeflow_event_status=timeflow_event_status,
            source_url=source_url,
            source_title=source_title,
        )
        if new_event:
            return new_event

    except Exception as e:
        raise ValueError(f"Error: {e}")
