import datetime
import os.path
import json
from app import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.shortcuts import render, redirect

app_name = 'main'

# Переделать на базу данных
def get_user_credentials(user_id):
    credentials = None
    user_creds_path = f"user_creds\{user_id}.json"

    with open(user_creds_path, 'r') as file:
        token = json.load(file)

    if os.path.exists(user_creds_path):
            credentials = Credentials(
                token=token['access_token'],
                refresh_token=token['refresh_token'],
                token_uri='https://oauth2.googleapis.com/token',
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                scopes=settings.SCOPES
            )
    else:
        # Переделать
        return None
    
    return credentials
