import pytz
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from scheduler.utils import schedule_tasks_for_user
from users.utils import get_hours_by_id
from users.models import Hours
from main.models import Color

from .utils import get_user_tasks, create_new_user_task, create_task_event
from .models import Task

# Create your views here.
@login_required
def get_tasks(request):
    user = request.user
    user_task_list = get_user_tasks(user)
    return JsonResponse({"tasks": user_task_list})

@login_required
def get_task_by_id(request, id):
    user = request.user
    try:
        task = Task.objects.get(user=user, id=id)
        return JsonResponse(task.to_json())
    except Task.DoesNotExist:
        raise ValueError("Task does not exist")
    except Exception as e:
        raise ValueError(f"Exception: {e}")


def create_task(request):
    """Create a new user task. Format: {
                                "name": task.name,
                                "priority": task.priority,
                                "duration": task.duration,
                                "min_duration"=task.min_duration,
                                "max_duration"=task.max_duration,
                                "schedule_after"=task.schedule_after or None,
                                "due_date": task.due_date,
                                "hours_id": task.hours.pk,
                                "color_id": int,
                                "private": task.private,
                                "notes": task.notes,
                                }"""
    try:
        params = request.GET
        user = request.user
        task_hours = get_hours_by_id(params['hours_id'])
        user_timezone = pytz.timezone(user.time_zone)
        
        schedule_after = datetime.fromisoformat(params['schedule_after']) if "schedule_after" in params else datetime.now()
        private = params['private'] if "private" in params else True
        min_duration = timedelta(minutes=int(params['min_duration'])) if 'min_duration' in params and params['min_duration'] else None
        max_duration = timedelta(minutes=int(params['max_duration'])) if 'max_duration' in params and params['min_duration'] else None
        color = Color.objects.get(id=params['colorId'])if 'color_id' in params and params['color_id'] else None
        notes = params['notes'] if 'notes' in params else ''

        due_date_aware = user_timezone.localize(datetime.fromisoformat(params['due_date']))

        task = create_new_user_task(user, 
                name=params['name'], 
                priority=params['priority'], 
                duration=timedelta(minutes=int(params["duration"])), 
                min_duration=min_duration, 
                max_duration=max_duration,
                schedule_after=schedule_after,
                due_date=due_date_aware,
                hours=task_hours,
                private=private,
                color=color,
                notes=notes,
                )
        
        scheduled_tasks = schedule_tasks_for_user(user)
            
        return JsonResponse({"created": True, "task": task.to_json()})
        
    except Hours.DoesNotExist:
        raise ValueError("Hours id does not match any existing objects.")
    except Exception as e:
            raise ValueError(f"{e}")
    

def test_task(request):
    user = request.user
    task = Task.objects.filter(user=user).last()
    start = datetime.now()
    end = datetime.now() + timedelta(minutes=45)
    event = create_task_event(task, start_datetime=start, end_datetime=end)
    return JsonResponse({"success": f'{event}'})
