from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    return render(request, "index.html")

@login_required
def get_habits(request):
    return JsonResponse({})

@login_required
def get_habit_by_id(request, id):
    return JsonResponse({})