from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Task


# Create your views here.
@login_required
def get_tasks(request):
    user = request.user
    user_tasks = Task.objects.filter(user=user)
    user_task_list = []
    for task in user_tasks:
        user_task_list.append({"id": task.pk,
                                "name": task.name,
                                "priority": task.priority,
                                "time_needed": task.time_needed,
                                "due_date": task.due_date,
                                "hours": {"name": task.hours.name, "intervals": task.get_hours()},
                                "calendar": task.hours.calendar.summary,
                                "notes": task.notes,
                                })
    return JsonResponse({"tasks": user_task_list})

@login_required
def get_task_by_id(request, id):
    return NotImplementedError()

def create_task(request):
    return NotImplementedError()