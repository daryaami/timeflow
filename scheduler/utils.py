import datetime
from datetime import date, datetime, timedelta
from tasks.models import Task
from planner.utils import get_all_user_events

SCHEDULE_INTERVAL_DAYS = 90


class TaskToSchedule:
    def __init__(self, name, duration, deadline, work_hours, max_block_duration):
        self.name = name
        self.duration = duration
        self.deadline = deadline
        self.work_hours = work_hours  # work_hours is a dict with days as keys and time intervals as values
        self.max_block_duration = max_block_duration
        self.blocks = []  # to store assigned time blocks


class TaskScheduler:
    def __init__(self, user):
        self.tasks = []
        self.calendar = self.load_user_calendar(user)  # This should be filled with existing calendar events

    def load_user_calendar(self, user):
        user_credentials = user.get_and_refresh_credentials()
        user_calendars = user.get_user_calendars()
        # Load existing calendar events for the user
        events = get_all_user_events(user_calendars=user_calendars, user_credentials=user_credentials, start_date=date.today(), time_interval=timedelta(days=SCHEDULE_INTERVAL_DAYS))
        calendar = [(event.get("start").get("dateTime"), event.get('end').get("dateTime")) for event in events]
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
                    work_start = current_date.replace(hour=interval[0].hour,
                                                    minute=interval[0].minute, second=0)
                    work_end = current_date.replace(hour=interval[1].hour,
                                                    minute=interval[1].minute, second=0)

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

            current_date += datetime.timedelta(days=1)

        return free_slots

    def schedule_tasks(self):
        # Sort tasks by priority and due date
        self.tasks.sort(key=lambda x: (x.priority, x.due_date))

        for task in self.tasks:
            duration_left = task.duration
            current_date = datetime.datetime.now().date()

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
                    task.blocks.append((slot_start, slot_start + datetime.timedelta(minutes=slot_duration)))
                    duration_left -= slot_duration
                    current_date = slot_start.date() + datetime.timedelta(minutes=slot_duration)

                    # Update calendar to reflect new booking
                    self.calendar.append((slot_start, slot_start + datetime.timedelta(minutes=slot_duration)))

                current_date += datetime.timedelta(days=1)  # move to next day

# Example usage
def schedule_tasks_for_user(user):
    scheduler = TaskScheduler(user)
    tasks = Task.objects.filter(user=user)
    for task in tasks:
        hours = task.hours
        work_hours = {day: [(datetime.time.fromisoformat(interval['start']), datetime.time.fromisoformat(interval['end'])) 
                            for interval in intervals] 
                    for day, intervals in hours.intervals.items()}
        new_task = TaskToSchedule(
            name=task.name,
            priority=task.priority,
            duration=task.time_needed,
            due_date=task.due_date,
            work_hours=work_hours,
            max_block_duration=task.max_duration
        )
        scheduler.add_task(new_task)

    scheduler.schedule_tasks()

    return scheduler.tasks