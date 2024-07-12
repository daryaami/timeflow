import datetime
from datetime import date, time, datetime, timedelta, timezone
from tasks.models import Task
import pytz 
from planner.utils import get_all_user_events

SCHEDULE_INTERVAL_DAYS = 90

class TaskScheduler:
    def __init__(self, user):
        self.user_timezone = pytz.timezone(user.time_zone)
        self.tasks = []
        self.calendar = self.load_user_calendar(user)  # This should be filled with existing calendar events

    def load_user_calendar(self, user):
        user_credentials = user.get_and_refresh_credentials()
        user_calendars = user.get_calendars()
        # Load existing calendar events for the user
        events = get_all_user_events(user_calendars=user_calendars, user_credentials=user_credentials, start_date=date.today(), time_interval=timedelta(days=SCHEDULE_INTERVAL_DAYS))
        calendar = [(datetime.fromisoformat(event.get("start").get("dateTime")).astimezone(self.user_timezone),
                    datetime.fromisoformat(event.get('end').get("dateTime")).astimezone(self.user_timezone)) for event in events]
        return sorted(calendar)

    def add_task(self, task):
        self.tasks.append(task)

    def find_free_slots(self, work_hours, start_date, end_date):
        free_slots = []
        current_date = start_date

        while current_date <= end_date:
            day_of_week = current_date.strftime("%A")
            if day_of_week in work_hours:
                for interval in work_hours[day_of_week]:
                    interval_start = time.fromisoformat(interval[0])
                    interval_end = time.fromisoformat(interval[1])
                    work_start = self.user_timezone.localize(datetime.combine(current_date, interval_start))
                    work_end = self.user_timezone.localize(datetime.combine(current_date, interval_end))

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
        # Sort tasks by priority and due date
        self.tasks.sort(key=lambda x: (x.priority, x.due_date))

        for task in self.tasks:
            duration_left = task.time_needed
            current_date = datetime.now(self.user_timezone).date()

            while duration_left > 0 and current_date <= task.due_date:
                free_slots = self.find_free_slots(task.work_hours, current_date, task.due_date)

                for slot in free_slots:
                    if duration_left <= 0:
                        break

                    slot_start, slot_end = slot
                    slot_duration = (slot_end - slot_start).seconds // 60

                    if slot_duration > task.max_duration:
                        slot_duration = task.max_duration

                    if slot_duration > duration_left:
                        slot_duration = duration_left

                    # Allocate time block to the task
                    task.blocks.append((slot_start, slot_start + timedelta(minutes=slot_duration)))
                    duration_left -= slot_duration
                    current_date = slot_start.date() + timedelta(minutes=slot_duration)

                    # Update calendar to reflect new booking
                    self.calendar.append((slot_start, slot_start + timedelta(minutes=slot_duration)))
                    print(self.calendar)

                current_date += timedelta(days=1)  # move to next day

# Example usage
def schedule_tasks_for_user(user):
    scheduler = TaskScheduler(user)
    tasks = Task.objects.filter(user=user)
    for task in tasks:
        work_hours = {day: [(interval['start'], interval['end']) for interval in intervals] for day, intervals in task.hours.intervals.items()}
        task.work_hours = work_hours
        task.blocks = []
        scheduler.add_task(task)

    scheduler.schedule_tasks()

    return scheduler.tasks