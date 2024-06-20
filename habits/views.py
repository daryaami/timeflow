from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def index(request):
    habits = [
        {'name': 'Exercise', 'duration': '30 mins'},
        {'name': 'Reading', 'duration': '1 hour'},
        {'name': 'Meditation', 'duration': '20 mins'},
        # добавьте остальные привычки
    ]
    context = {'habits': habits}
    return render(request, 'habits/habits.html', context)
