import os
import requests
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from users.models import GoogleCredentials, UserCalendar, CustomUser

