import datetime
from datetime import date, time, datetime, timedelta
from tasks.utils import create_task_event, get_user_tasks
from utils import LockState
from tasks.models import Task
from users.models import CustomUser
import pytz
from planner.utils import get_all_user_events
from django.http import JsonResponse

SCHEDULE_INTERVAL_DAYS = 60
priority_order = {None: 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


def get_sort_key(task):
    return (-priority_order[task.priority], task.due_date)


def timefromstring(time_str):
    """
    Преобразует строку времени в объект datetime.time.
    """
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError as e:
        print(f"Invalid time format: {time_str}. Error: {e}")
        return None


def round_up(dt, interval_minutes=15):
    add_minutes = interval_minutes - (dt.minute % interval_minutes)
    if add_minutes == interval_minutes:
        add_minutes = 0
    return dt + timedelta(
        minutes=add_minutes, seconds=-dt.second, microseconds=-dt.microsecond
    )


class TaskEvent:
    def __init__(self, tz=None, event=None, task=None, start=None, end=None):
        if event:
            self.start = datetime.fromisoformat(
                event.get("start").get("dateTime")
            ).astimezone(tz)
            self.end = datetime.fromisoformat(
                event.get("end").get("dateTime")
            ).astimezone(tz)
            self.timeflow_touched = True if "timeflow_touched" in event else False
            self.event_type = (
                event.get("timeflow_event_type") if self.timeflow_touched else None
            )
            self.event_id = (
                event.get("timeflow_event_id") if self.timeflow_touched else None
            )
            self.event_priority = (
                event.get("timeflow_event_priority") if self.timeflow_touched else None
            )
        if task:
            self.start = start
            self.end = end
            self.timeflow_touched = True
            self.event_id = str(task.pk)
            self.event_type = "0"
            self.event_priority = task.priority
        self.timespent = 0

    def to_json(self):
        return {
            "start": self.start,
            "end": self.end,
            "task_id": self.event_id,
            "timeflow_touched": self.timeflow_touched,
        }


class TaskScheduler:
    """
    Планировщик задач для пользователя.

    Attributes:
        user_timezone (timezone): Временная зона пользователя.
        tasks (list): Список задач.
        calendar (list): Календарь пользователя с событиями.
    """

    def __init__(self, user):
        """
        Инициализация TaskScheduler с данными пользователя.

        Args:
            user (User): Объект пользователя.
        """
        self.user_timezone = pytz.timezone(user.time_zone)
        self.calendar = self.load_user_calendar(user)
        self.tasks = []

    def load_user_calendar(self, user):
        """
        Загружает календарь пользователя.

        Args:
            user (User): Объект пользователя.

        Returns:
            list: Список событий в календаре.
        """
        user_credentials = user.get_and_refresh_credentials()
        events = get_all_user_events(
            user=user,
            credentials=user_credentials,
            start_date=date.today() - timedelta(days=SCHEDULE_INTERVAL_DAYS),
            time_interval=timedelta(days=SCHEDULE_INTERVAL_DAYS * 2),
        )
        calendar = [
            TaskEvent(event=event, tz=self.user_timezone)
            for event in events
            if "dateTime" in event["start"]
        ]
        calendar.sort(key=lambda x: x.start)
        return calendar

    def add_event(self, event):
        self.calendar.append(event)
        self.calendar.sort(key=lambda x: x.start)

    def add_task(self, task: Task):
        task_calendar_events = list(
            filter(lambda event: event.event_id == str(task.pk), self.calendar)
        )
        total_event_duration = sum(
            ((event.end - event.start) for event in task_calendar_events), timedelta()
        )
        task.duration -= total_event_duration
        print(
            f"{task.name}: duration left {task.duration}, already planned {total_event_duration}"
        )
        if task.duration > timedelta(0):
            task.min_duration = min(task.min_duration, task.duration)
            self.tasks.append(task)

    def find_free_slots(self, available_hours, start_datetime, end_datetime, task):
        free_slots = []
        current_datetime = start_datetime + timedelta(minutes=5)

        day_to_intervals = {}
        for day, intervals in available_hours.items():
            day_to_intervals[day] = [(timefromstring(i['start']), timefromstring(i['end'])) for i in intervals]

        while current_datetime <= end_datetime:
            day_of_week = current_datetime.strftime("%A")
            if day_of_week in day_to_intervals:
                intervals = day_to_intervals[day_of_week]
                for interval_start, interval_end in intervals:
                    if interval_start is None or interval_end is None:
                        continue

                    work_start = self.user_timezone.localize(datetime.combine(current_datetime.date(), interval_start))
                    work_end = self.user_timezone.localize(datetime.combine(current_datetime.date(), interval_end))
                    slot_start = max(work_start, round_up(current_datetime))

                    for event in self.calendar:
                        if event.start >= work_end:
                            break
                        if event.start < slot_start:
                            if event.end > current_datetime:
                                slot_start = event.end
                            continue
                        else:
                            if event.start > slot_start:
                                free_slots.append((slot_start, event.start))
                            slot_start = min(event.end, work_end)

                    if slot_start < work_end:
                        free_slots.append((slot_start, work_end))

            current_datetime = (current_datetime + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)

        return free_slots

    def schedule_tasks(self):
        """
        Планирует задачи, распределяя их по доступным временным слотам.
        """
        self.tasks.sort(key=get_sort_key)

        for task in self.tasks:
            duration_left = task.duration
            current_datetime = datetime.now(self.user_timezone)
            max_duration = min(task.duration, task.max_duration)
            min_duration = task.min_duration

            while duration_left > timedelta(0) and current_datetime <= task.due_date:
                free_slots = self.find_free_slots(
                    available_hours=task.available_hours,
                    start_datetime=max(current_datetime, task.schedule_after),
                    end_datetime=task.due_date,
                    task=task,
                )

                for slot in free_slots:
                    if duration_left <= timedelta(0):
                        break

                    slot_start, slot_end = slot
                    slot_duration = slot_end - round_up(slot_start)

                    if slot_duration > max_duration:
                        slot_duration = max_duration

                    if slot_duration < min_duration:
                        continue

                    if slot_duration > duration_left:
                        slot_duration = duration_left

                    task.blocks.append(
                        (round_up(slot_start), round_up(slot_start) + slot_duration)
                    )
                    new_event = TaskEvent(
                        tz=self.user_timezone,
                        start=round_up(slot_start),
                        end=round_up(slot_start) + slot_duration,
                        task=task,
                    )
                    self.add_event(event=new_event)
                    duration_left -= slot_duration
                    current_datetime = slot_start.date() + slot_duration

                current_datetime += timedelta(days=1)


def schedule_tasks_for_user(user):
    """
    Планирует задачи для пользователя.
    Args:
        user (User): Объект пользователя.

    Returns:
        list: Список задач с обновленными блоками времени.
    """
    scheduler = TaskScheduler(user)
    tasks = get_user_tasks(user=user)
    for task in tasks:
        task.available_hours = task.hours.intervals
        task.blocks = []
        scheduler.add_task(task)

    scheduler.schedule_tasks()
    events = []

    for task in scheduler.tasks:
        for block in task.blocks:
            new_event = create_task_event(
                task, block[0], block[1], status=LockState.FREE
            )
            events.append(new_event)

    return events
