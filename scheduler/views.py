from django.http import JsonResponse
from scheduler.utils import schedule_tasks_for_user
from tasks.utils import create_task_event

# Create your views here.
def scheduler(request):
    user = request.user
    tasks = schedule_tasks_for_user(user)

    for task in tasks:
        for block in task.blocks:
            create_task_event(task, block[0], block[1])
    
    return JsonResponse({"tasks": [task.blocks for task in tasks]})