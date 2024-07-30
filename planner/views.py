from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build

from planner.utils import get_all_events_by_weekday
from app import settings
from google_auth.exceptions import *

scopes = settings.SCOPES

@login_required
def get_events(request):
    user = request.user
    try:
        # Получение пользовательских учетных данных
        user_credentials = user.get_and_refresh_credentials()

        date_param = request.GET.get("date", None)
        events_by_days = get_all_events_by_weekday(
            user=user,
            credentials=user_credentials,
            date_param=date_param,
        )

        return JsonResponse(events_by_days)

    # 401 - нет учетных данных, нужна регистрация
    # 402 - не действительный refresh token, нужно обновление учетных данных
    # 403 - ошибка обновления токена, нужно обновление учетных данных 
    # 500 - сетевая или другая ошибка
    except CredentialsNotFoundError as e:
        # Credentials не найдены
        return JsonResponse({"error": str(e)}, status=401)

    except RefreshTokenMissing as e:
        # Refresh token не найден
        return JsonResponse({"error": str(e)}, status=402)

    except InvalidGrantError as e:
        # Недействительный refresh_token или ошибка безопасности
        return JsonResponse({"error": str(e)}, status=402)
    
    except TokenRefreshError as e:
        # Ошибка обновления Access токена
        return JsonResponse({"error": str(e)}, status=402)

    except RequestError as e:
        # Обработка сетевых ошибок
        return JsonResponse({"error": str(e)}, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
def update_event(user_credentials, calendar_id, event_id, updated_event_details):
    try:
        calendar_service = build("calendar", "v3", credentials=user_credentials)
        event = (
            calendar_service.events()
            .update(
                calendarId=calendar_id, eventId=event_id, body=updated_event_details
            )
            .execute()
        )
        return event
    except Exception as e:
        return e