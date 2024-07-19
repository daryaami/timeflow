import datetime
from datetime import date, time, datetime, timedelta, timezone
from tasks.models import Task
import pytz
from planner.utils import get_all_user_events

SCHEDULE_INTERVAL_DAYS = 90


def timefromstring(time_str):
    """
    Преобразует строку времени в объект datetime.time.

    Args:
        time_str (str): Время в формате "HH:MM".
    Returns:
        datetime.time: Объект времени.
    """
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError as e:
        print(f"Invalid time format: {time_str}. Error: {e}")
        return None


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
        self.tasks = []
        self.calendar = self.load_user_calendar(user)

    def load_user_calendar(self, user):
        """
        Загружает календарь пользователя.

        Args:
            user (User): Объект пользователя.

        Returns:
            list: Список событий в календаре.
        """
        try:
            user_credentials = user.get_and_refresh_credentials()
            user_calendars = user.get_calendars()
            events = get_all_user_events(
                user_calendars=user_calendars,
                user_credentials=user_credentials,
                start_date=date.today(),
                time_interval=timedelta(days=SCHEDULE_INTERVAL_DAYS),
            )
            calendar = [
                (
                    datetime.fromisoformat(
                        event.get("start").get("dateTime")
                    ).astimezone(self.user_timezone),
                    datetime.fromisoformat(event.get("end").get("dateTime")).astimezone(
                        self.user_timezone
                    ),
                )
                for event in events
            ]
            return sorted(calendar)
        except Exception as e:
            print(f"Error loading calendar: {e}")
            return []

    def add_task(self, task):
        self.tasks.append(task)

    def find_free_slots(self, work_hours, start_date, end_date):
        """
        Ищет свободные временные слоты в расписании.

        Args:
            work_hours (dict): Рабочие часы для каждого дня недели.
            start_date (date): Дата начала поиска.
            end_date (date): Дата окончания поиска.

        Returns:
            list: Список свободных временных слотов.
        """
        free_slots = []
        current_date = start_date

        while current_date <= end_date:
            day_of_week = current_date.strftime("%A")
            if day_of_week in work_hours:
                for interval in work_hours[day_of_week]:
                    interval_start = timefromstring(interval[0])
                    interval_end = timefromstring(interval[1])
                    work_start = self.user_timezone.localize(
                        datetime.combine(current_date, interval_start)
                    )
                    work_end = self.user_timezone.localize(
                        datetime.combine(current_date, interval_end)
                    )

                    slot_start = work_start

                    for event_start, event_end in self.calendar:
                        if event_start.date() != current_date:
                            continue
                        if event_start >= work_end:
                            break
                        if event_start >= slot_start and event_start < work_end:
                            if event_start > slot_start:
                                free_slots.append((slot_start, event_start))
                            slot_start = event_end

                    if slot_start < work_end:
                        free_slots.append((slot_start, work_end))

            current_date += timedelta(days=1)

        return free_slots

    def schedule_tasks(self):
        """
        Планирует задачи, распределяя их по доступным временным слотам.
        """
        self.tasks.sort(key=lambda x: (x.priority, x.due_date))

        for task in self.tasks:
            duration_left = task.duration
            current_date = datetime.now(self.user_timezone)
            max_duration = task.max_duration if task.max_duration else task.duration

            while duration_left > 0 and current_date <= task.due_date:
                free_slots = self.find_free_slots(
                    task.work_hours, current_date, task.due_date
                )

                for slot in free_slots:
                    if duration_left <= 0:
                        break

                    slot_start, slot_end = slot
                    slot_duration = (slot_end - slot_start).seconds // 60

                    if slot_duration > max_duration:
                        slot_duration = max_duration

                    if slot_duration > duration_left:
                        slot_duration = duration_left

                    task.blocks.append(
                        (slot_start, slot_start + timedelta(minutes=slot_duration))
                    )
                    duration_left -= slot_duration
                    current_date = slot_start.date() + timedelta(minutes=slot_duration)

                    self.calendar.append(
                        (slot_start, slot_start + timedelta(minutes=slot_duration))
                    )

                current_date += timedelta(days=1)


def schedule_tasks_for_user(user):
    """
    Планирует задачи для пользователя.

    Args:
        user (User): Объект пользователя.

    Returns:
        list: Список задач с обновленными блоками времени.
    """
    scheduler = TaskScheduler(user)
    tasks = Task.objects.filter(user=user)
    for task in tasks:
        work_hours = {
            day: [(interval["start"], interval["end"]) for interval in intervals]
            for day, intervals in task.hours.intervals.items()
        }
        task.work_hours = work_hours
        task.blocks = []
        scheduler.add_task(task)

    scheduler.schedule_tasks()

    return scheduler.tasks
