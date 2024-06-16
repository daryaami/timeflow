from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import json
from app import settings

# Create your views here.
def index(request):
    return render(request, "google_auth/index.html")


def google_auth_redirect(request):
    scope = "https://www.googleapis.com/auth/calendar.events"
    auth_uri = "https://accounts.google.com/o/oauth2/v2/auth"
    response_type = "code"

    auth_url = (
        f"{auth_uri}"
        f"?client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.AUTH_REDIRECT_URI}"
        f"&scope={scope}"
        f"&response_type={response_type}"
        f"&access_type=offline"
        f"&prompt=consent"  # убрать
    )
    return redirect(auth_url)


def oauth2callback(request):
    code = request.GET.get("code")

    if code:
        token_url = "https://accounts.google.com/o/oauth2/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.AUTH_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            
            json.dump(token_data, open("user_creds/1.json", 'w'))
            # access_token = token_data.get("access_token")
            # refresh_token = token_data.get("refresh_token")

            # if refresh_token:
            #     with open("refresh.txt", 'w') as file:
            #         file.write(str(refresh_token))

            return JsonResponse({"token_data": token_data})
        else:
            return JsonResponse(
                {"error": "Failed to retrieve access token"},
                status=response.status_code,
            )

    return JsonResponse({"error": "No authorization code provided"}, status=400)


def refresh_access_token(request):

    with open("refresh.txt", 'r') as file:
        refresh_token = file.readline().strip()
    
    # return JsonResponse({"token": refresh_token})

    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }

    response = requests.post(token_url, data=data)
    response_data = response.json()

    if "access_token" in response_data:
        return JsonResponse({"access_token": response_data["access_token"]})
        return response_data["access_token"]
    else:
        raise Exception("Could not refresh access token")
