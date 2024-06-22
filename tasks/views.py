from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def index(request):
    # tasks = [
    #     {
    #         'name': 'Task 1',
    #         'duration': '2 hours',
    #         'deadline': '2024-06-20 10:00'
    #     },
    #     {
    #         'name': 'Task 2',
    #         'duration': '3 hours',
    #         'deadline': '2024-06-21 14:00'
    #     },
    #     {
    #         'name': 'Task 3',
    #         'duration': '1 hour',
    #         'deadline': '2024-06-22 09:00'
    #     },
    #     {
    #         'name': 'Task 4',
    #         'duration': '4 hours',
    #         'deadline': '2024-06-23 16:00'
    #     },
    #     {
    #         'name': 'Task 5',
    #         'duration': '5 hours',
    #         'deadline': '2024-06-24 11:00'
    #     },
    # ]
    # context = {'tasks': tasks}
    
    # return render(request, 'tasks/tasks.html', context)
    return render(request, "index.html")
