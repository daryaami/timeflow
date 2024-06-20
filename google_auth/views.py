from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import json
from app import settings
import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from django import urls


from app import settings


def google_auth_redirect(request):
    scopes = settings.SCOPES
    scope = " ".join(scopes)
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

    return JsonResponse({'response': response.json()})

    if response.status_code == 200:
        token_data = response.json()

        return JsonResponse({'token': token_data})

        json.dump(token_data, open("user_creds/1.json", "w"))

        # id_token = token_data.get("id_token")

        # if id_token:
        #     decoded_id_token = decode_id_token(id_token, settings.GOOGLE_CLIENT_ID)
            
        # http = redirect("main:planner")
        # http.set_cookie('auth_token', decoded_id_token['sub'], max_age=None)
        # return http
        return JsonResponse({"token_data": token_data})

    # else:
    #     return JsonResponse({'error': "Failed to retrieve access token"})  # исправить на консоль


def refresh_access_token(request):
    with open("refresh.txt", "r") as file:
        refresh_token = file.readline().strip()
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
    else:
        raise Exception("Could not refresh access token")


def get_google_public_keys():
    response = requests.get("https://www.googleapis.com/oauth2/v3/certs")
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Could not retrieve public keys from Google")


def decode_id_token(id_token, audience, leeway=10810):
    public_keys = get_google_public_keys()
    header = jwt.get_unverified_header(id_token)
    key_id = header["kid"]

    public_key = None
    for key in public_keys["keys"]:
        if key["kid"] == key_id:
            public_key = RSAAlgorithm.from_jwk(key)
            break

    if public_key is None:
        raise ValueError("Public key not found")

    try:
        decoded_token = jwt.decode(
            id_token, public_key, algorithms=["RS256"], audience=audience, leeway=leeway
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidAudienceError:
        raise ValueError("Invalid audience")
    except jwt.ImmatureSignatureError:
        raise ValueError("The token is not yet valid (iat)")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")



# 
# {"token_data": {"access_token": "ya29.a0AXooCgvU750ekRYNhC0b-3F84PbtiUWa-s5yl0OiqZEZporRx_6Z3UzJJfJFYI3t8Hp1pEx33ZhYAdgUJVtEy1EQrzLrz_hX6QxIVzsCoi43ALykRmiYfwAB0j6xxW6OO7I5xSgOr51IcSteiz9UqbNbig6RJxj7u6noaCgYKAWsSARESFQHGX2MiY_Oofp3e8sK7hQVXbbVVCw0171", "expires_in": 3599, "refresh_token": "1//0cbsJ8iL66xVeCgYIARAAGAwSNwF-L9IrkOlBX9tHKwI3_rHJR_RGm7WQiwX1sBxCcUcvNBzI7tzRfrekhVxoqXFdSpSa9NZpVFc", "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/calendar.events openid", "token_type": "Bearer", "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNkNTgwZjBhZjdhY2U2OThhMGNlZTdmMjMwYmNhNTk0ZGM2ZGJiNTUiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiYXpwIjoiNzYwNjM1Nzk4MjIxLWdzODY4ZWU0cHFibzZyNDdmOWNoc2gzMTBnMjltamxmLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiNzYwNjM1Nzk4MjIxLWdzODY4ZWU0cHFibzZyNDdmOWNoc2gzMTBnMjltamxmLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTAzMjQ0NTIwMTM1NzYzMjAzNjMxIiwiZW1haWwiOiJkYXJ5YWFtaTEwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoidENzT1BpUXFvM1JNTFJGdTRwRFRfQSIsImlhdCI6MTcxODc0MzI2OCwiZXhwIjoxNzE4NzQ2ODY4fQ.PR0wxTRv0RJLLHlhtOB6AIe6qRDKvjOydQAEpXmtwuGOC8Wt2XN0tonviT1Itby-oFUHFx-CL3GR3Gma72AbPPxGhEVt-vshcGpqEVkkKpL5mpZGk0lOn6x8fj6MmjzoUaKY6funTKgtHl3CSFOMXu3dVm3gRPF9olT_wSPDT3TD7IaFyyMjJM2WdIYyg6tBAq7mGSZNJIFu0wIQDCwJNntCmyFRugGvBBBK9-lVpppJcWAcOi_90-rZGHR3g4d_u_7F2UYUX-TPYKdXnOa54zvgSqQcobd2r3Iv0FpEGltZXMYYYTYJQIAgXfucouRxKS3udWtAkQki2uImd3bvqQ"}, 
# "decoded_id_token": {"iss": "accounts.google.com", 
# "azp": "760635798221-gs868ee4pqbo6r47f9chsh310g29mjlf.apps.googleusercontent.com", 
# "aud": "760635798221-gs868ee4pqbo6r47f9chsh310g29mjlf.apps.googleusercontent.com", 
# "sub": "103244520135763203631", "email": "daryaami10@gmail.com", 
# "email_verified": true, "at_hash": "tCsOPiQqo3RMLRFu4pDT_A", 
# "iat": 1718743268, "exp": 1718746868}}


