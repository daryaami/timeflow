from django.utils import timezone
from datetime import timedelta
import os
import requests
from django.shortcuts import redirect
from django.contrib.auth import login
from django.http import JsonResponse
from app import settings
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from users.models import GoogleCredentials, UserCalendar, CustomUser
from users.utils import create_user_custom_hours
from .utils import (
    create_flow,
    get_userinfo_from_endpoint,
    register_new_user,
    set_user_calendars_and_timezone,
)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def log_in(request):
    flow = create_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
    )

    request.session["state"] = state
    request.session["type"] = "login"
    return redirect(authorization_url)


def login_callback(request):
    state = request.session["state"]

    flow = create_flow(state=state)
    flow.fetch_token(authorization_response=request.get_full_path())
    credentials = flow.credentials

    # Использование userinfo endpoint для получения информации о пользователе
    user_info = get_userinfo_from_endpoint(credentials=credentials)
    email = user_info["email"]

    try:
        user = CustomUser.objects.get(email=email)
        refreshed_creds = user.get_and_refresh_credentials()
        user_credentials = GoogleCredentials.objects.get(user=user)

        if refreshed_creds and user_credentials.is_valid():
            login(request, user)
            return redirect("main:planner")
        else:
            return redirect("auth:refresh_permissions")
        
    except CustomUser.DoesNotExist:
        return redirect("auth:register")

    except GoogleCredentials.DoesNotExist:
        return redirect("auth:refresh_permissions")

    except Exception as e:
        return JsonResponse({"error": str(e)})


def register(request):
    flow = flow = create_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )

    request.session["state"] = state
    request.session["type"] = "register"
    return redirect(authorization_url)


def register_callback(request):
    state = request.session["state"]

    flow = create_flow(state=state)
    flow.fetch_token(authorization_response=request.get_full_path())
    credentials = flow.credentials

    # Использование userinfo endpoint для получения информации о пользователе
    user_info = get_userinfo_from_endpoint(credentials=credentials)
    email = user_info["email"]

    try:
        user = CustomUser.objects.get(email=email)
        return redirect("auth:log_in")
    except CustomUser.DoesNotExist:
        user_created = register_new_user(user_info=user_info)

        if not user_created[1]:
            raise ValueError("Could now register user.")
        
        user = user_created[0]

        # Создать учетные данные
        GoogleCredentials.objects.update_or_create(
            user=user,
            defaults={
                "access_token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "token_uri": credentials.token_uri,
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "scopes": ",".join(credentials.scopes),
                "expiry": credentials.expiry,
            },
        )

        # Добавить выбор календарей
        set_user_calendars_and_timezone(user=user, credentials=credentials)

        # Создание базовых часов пользователя - дефолтный календарь основной
        create_user_custom_hours(user=user)

    except Exception as e:
        return e
    
    finally:
        user = CustomUser.objects.get(email=email)
        login(request, user)
        return redirect("main:planner")


def refresh_permissions(request):
    flow = create_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )

    request.session["state"] = state
    request.session["type"] = "refresh_permissions"
    return redirect(authorization_url)


def refresh_permissions_callback(request):
    state = request.session["state"]
    flow = create_flow(state=state)

    flow.fetch_token(authorization_response=request.get_full_path())
    credentials = flow.credentials

    # Использование userinfo endpoint для получения информации о пользователе - вынести в функцию
    user_info = get_userinfo_from_endpoint(credentials=credentials)
    email = user_info["email"]

    try:
        user = CustomUser.objects.get(email=email)

        GoogleCredentials.objects.update_or_create(
            user=user,
            defaults={
                "access_token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "token_uri": credentials.token_uri,
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "scopes": ",".join(credentials.scopes),
                "expiry": credentials.expiry,
            },
        )

        if not user.image:
            user.image = user_info['picture']
            user.save()

        set_user_calendars_and_timezone(user, credentials=credentials)
        create_user_custom_hours(user)

        login(request, user)
        return redirect("main:index")
    
    except CustomUser.DoesNotExist:
        return redirect("auth:register")

    except Exception as e:
        raise ValueError(f"Something went wrong: {e}")
    

def google_oauth(request):
    state = request.session["state"]

    flow = create_flow(state=state)
    flow.fetch_token(authorization_response=request.get_full_path())
    credentials = flow.credentials

    # Использование userinfo endpoint для получения информации о пользователе
    user_info = get_userinfo_from_endpoint(credentials=credentials)
    email = user_info["email"]

    try:
        user = CustomUser.objects.get(email=email)
        refreshed_creds = user.get_and_refresh_credentials()
        user_credentials = GoogleCredentials.objects.get(user=user)

        if refreshed_creds and user_credentials.is_valid():
            login(request, user)
            return redirect("main:planner")
        else:
            redirect("auth:refresh_permissions")
        
    except CustomUser.DoesNotExist:
        user_created = register_new_user(user_info=user_info)
        if not user_created[1]:
            raise ValueError("Could now register user.")

    except GoogleCredentials.DoesNotExist:
        redirect("auth:refresh_permissions")

    # Update or create GoogleCredentials
    new_credentials = GoogleCredentials.objects.update_or_create(
        user=user,
        defaults={
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": ",".join(credentials.scopes),
            "expiry": credentials.expiry,
        },
    )

    if not new_credentials[1]:
        raise ValueError("Could not update or create user credentials.")

    # Добавить выбор календарей
    set_user_calendars_and_timezone(user=user, credentials=credentials)

    # Создание базовых часов пользователя
    create_user_custom_hours(user=user)

    # Вход пользователя в Planner
    login(request, user)
    return redirect("main:planner")


# def register(request):
#     flow = flow = create_flow()

#     authorization_url, state = flow.authorization_url(
#         access_type="offline",
#         prompt="consent",
#     )

#     request.session["state"] = state
#     request.session["type"] = "register"
#     return redirect(authorization_url)

# def create_superuser_profile(request):
#     user = request.user

