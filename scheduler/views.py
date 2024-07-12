from django.http import JsonResponse, HttpResponseRedirect
from users.models import GoogleCredentials
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build

from planner.utils import get_all_events_by_weekday
from app import settings

from datetime import datetime, timedelta, time
import json
from datetime import datetime, timedelta

from scheduler.utils import TaskScheduler
from scheduler.utils import schedule_tasks_for_user


# Create your views here.
def scheduler(request):
    user = request.user
    tasks = schedule_tasks_for_user(user)
    return JsonResponse({"tasks": [task.blocks for task in tasks]})