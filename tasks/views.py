import json
import pytz
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from scheduler.utils import schedule_tasks_for_user
from users.utils import get_hours_by_id
from django.utils import timezone
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

@login_required
def create_task(request):
    """Create a new user task. Format: {
                                "name": task.name,
                                "priority": task.priority,
                                "duration": task.duration,
                                "min_duration": task.min_duration,
                                "max_duration": task.max_duration,
                                "schedule_after": task.schedule_after or None,
                                "due_date": task.due_date,
                                "hours_id": task.hours.pk,
                                "color_id": int,
                                "private": task.private,
                                "notes": task.notes,
                                }"""
    if request.method != 'POST':
            return JsonResponse({"error": "Only POST requests are allowed."}, status=405)
    
    try:
        params = json.loads(request.body.decode('utf-8'))
        user = request.user
        task_hours = get_hours_by_id(params['hours_id'])
        user_timezone = pytz.timezone(user.time_zone)
        
        schedule_after = datetime.fromisoformat(params['schedule_after']) if "schedule_after" in params else timezone.now()
        private = params.get('private', True)
        min_duration = timedelta(minutes=int(params['min_duration'])) if 'min_duration' in params and params['min_duration'] else None
        max_duration = timedelta(minutes=int(params['max_duration'])) if 'max_duration' in params and params['max_duration'] else None
        color = Color.objects.get(id=params['color_id']) if 'color_id' in params and params['color_id'] else None
        notes = params.get('notes', '')

        # due_date_aware = user_timezone.localize(datetime.fromisoformat(params['due_date']))
        due_date_aware = datetime.fromisoformat(params['due_date']).astimezone(user_timezone)
        print(f"Due date: {params['due_date']}, Due date aware: {due_date_aware}")

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
        return JsonResponse({"error": "Hours id does not match any existing objects."}, status=400)
    except Color.DoesNotExist:
        return JsonResponse({"error": "Color id does not match any existing objects."}, status=400)
    # except KeyError as e:
    #     return JsonResponse({"error": f"Missing parameter: {e.args[0]}"}, status=400)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    # except Exception as e:
    #     return JsonResponse({"error": "An unexpected error occurred."}, status=500)
    

def test_task(request):
    user = request.user
    task = Task.objects.filter(user=user).last()
    start = datetime.now()
    end = datetime.now() + timedelta(minutes=45)
    event = create_task_event(task, start_datetime=start, end_datetime=end)
    return JsonResponse({"success": f'{event}'})
