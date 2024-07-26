from django.http import JsonResponse
from scheduler.utils import schedule_tasks_for_user
from tasks.utils import create_task_event
from utils import LockState

# Create your views here.
def schedule_tasks(request):
    user = request.user
    tasks = schedule_tasks_for_user(user)
    return JsonResponse({"tasks": [task.blocks for task in tasks]})