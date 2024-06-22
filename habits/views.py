from django.shortcuts import render
import json
from django.http import JsonResponse
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date, parse_time
from .models import Habit


# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")

@login_required
def get_habits(request):
    user = request.user
    try:
        habits = Habit.objects.filter(user=user)
        habits_list = []
        
        for habit in habits:
            habit_data = {
                "name": habit.name,
                "priority": habit.priority,
                "min_duration": habit.min_duration,
                "max_duration": habit.max_duration,
                "category": habit.category,
                "period": habit.period,
                "times_per_period": habit.times_per_period,
                "ideal_days": habit.ideal_days,
                "ideal_time": habit.ideal_time,
                "starting": habit.starting,
                "ending": habit.ending,
                "visibility": habit.visibility,
                "notes": habit.notes,
            }
            habits_list.append(habit_data)
        
        return JsonResponse({"habits": habits_list})
    except Habit.DoesNotExist:
        return JsonResponse({"habits": []})

@login_required
def get_habit_by_id(request, id):
    user = request.user
    try:
        habit = Habit.objects.get(id=id, user=user)
        habit_data = {
            "name": habit.name,
            "priority": habit.priority,
            "min_duration": habit.min_duration,
            "max_duration": habit.max_duration,
            "category": habit.category,
            "period": habit.period,
            "times_per_period": habit.times_per_period,
            "ideal_days": habit.ideal_days,
            "ideal_time": habit.ideal_time,
            "starting": habit.starting,
            "ending": habit.ending,
            "visibility": habit.visibility,
            "notes": habit.notes,
        }
        return JsonResponse({"habit": habit_data})
    except Habit.DoesNotExist:
        return JsonResponse({"error": "Habit not found"}, status=404)
    

@login_required
def add_habit(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        
        name = data.get('name')
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        
        priority = data.get('priority', 'high')
        min_duration = data.get('min_duration', 30)
        max_duration = data.get('max_duration', 60)
        category = data.get('category', 'personal')
        period = data.get('period', 'weekly')
        times_per_period = data.get('times_per_period', 1)
        ideal_days = data.get('ideal_days', [])
        ideal_time = data.get('ideal_time', '08:00')
        starting = parse_date(data.get('starting', str(date.today())))
        ending = data.get('ending', None)
        
        if ending:
            ending = parse_date(ending)
        
        visibility = data.get('visibility', 'Busy')
        notes = data.get('notes', '')
        
        habit = Habit.objects.create(
            name=name,
            priority=priority,
            min_duration=min_duration,
            max_duration=max_duration,
            category=category,
            period=period,
            times_per_period=times_per_period,
            ideal_days=ideal_days,
            ideal_time=datetime.strptime(ideal_time, '%H:%M').time(),
            starting=starting,
            ending=ending,
            visibility=visibility,
            notes=notes,
            user=request.user
        )
        
        return JsonResponse({'habit': {
            'name': habit.name,
            'priority': habit.priority,
            'min_duration': habit.min_duration,
            'max_duration': habit.max_duration,
            'category': habit.category,
            'period': habit.period,
            'times_per_period': habit.times_per_period,
            'ideal_days': habit.ideal_days,
            'ideal_time': habit.ideal_time,
            'starting': habit.starting.isoformat(),
            'ending': habit.ending.isoformat() if habit.ending else None,
            'visibility': habit.visibility,
            'notes': habit.notes
        }}, status=201)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)