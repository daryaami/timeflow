from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import pytz

# from django.utils import timezone
from .models import Task
from .utils import get_user_tasks, create_new_user_task
from users.utils import get_hours_by_id
from users.models import Hours

# Create your views here.
@login_required
def get_tasks(request):
    user = request.user
    user_task_list = get_user_tasks(user)
    return JsonResponse({"tasks": user_task_list})

@login_required
def get_task_by_id(request, id):
    return NotImplementedError()

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
        min_duration = int(params['min_duration']) if 'min_duration' in params else None
        max_duration = int(params['max_duration']) if 'max_duration' in params else None

        due_date_aware = user_timezone.localize(datetime.fromisoformat(params['due_date']))

        task = create_new_user_task(user, 
                name=params['name'], 
                priority=params['priority'], 
                duration=int(params["duration"]), 
                min_duration=min_duration, 
                max_duration=max_duration,
                schedule_after=schedule_after,
                due_date=due_date_aware,
                hours=task_hours,
                private=private,)
            
        return JsonResponse({"created": True, "task": task.to_json()})
        
    except Hours.DoesNotExist:
        raise ValueError("Hours id does not match any existing objects.")
    except Exception as e:
            raise ValueError(f"{e}")