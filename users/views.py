import os
import requests
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from django.http import JsonResponse
from users.models import GoogleCredentials, UserCalendar, CustomUser, Hours
from tasks.models import Task
from tasks.utils import get_user_tasks_json
from .utils import get_user_hours_json


def get_user_info(request):
    user = request.user
    user_info = {
        "profile": user.get_profile_json(),
        "hours": get_user_hours_json(user=user),
        "tasks": get_user_tasks_json(user=user)
    }
    return JsonResponse(user_info)


def get_user_hours(request):
    user = request.user
    hours_json = {
        "user": user.email,
        "hours": [hours.to_json() for hours in user.get_user_hours_list()]
    }
    return hours_json