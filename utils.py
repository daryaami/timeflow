from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import timedelta
from django.utils import timezone
import requests
from app import settings
from django.shortcuts import redirect

# from users.models import GoogleCredentials
from google.auth.exceptions import RefreshError
from django.http import HttpResponseRedirect


# def get_and_refresh_user_credentials(user):
#     user_credentials = GoogleCredentials.objects.filter(user=user).first()

#     if not user_credentials:
#         return ValueError("User credentials not found.")
    
#     if user_credentials.refresh_token:
#         if user_credentials.access_token_expiry < timezone.now():
#             try:
#             # Refresh the access token
#                 refresh_request = requests.post(
#                         settings.TOKEN_URI,
#                         data={
#                             "client_id": user_credentials.client_id,
#                             "client_secret": user_credentials.client_secret,
#                             "refresh_token": user_credentials.refresh_token,
#                             "grant_type": "refresh_token",
#                         },
#                     )
                
#                 if refresh_request.status_code != 200:
#                     return ValueError(f"Failed to refresh token: {refresh_request.status_code}, {refresh_request.text}")

#                 new_credentials = refresh_request.json()

#                 user_credentials.access_token = new_credentials.get("access_token")
#                 user_credentials.access_token_expiry = timezone.now() + timedelta(seconds=new_credentials["expires_in"])
#                 user_credentials.save()

#                 credentials = Credentials(
#                     token=user_credentials.access_token,
#                     refresh_token=user_credentials.refresh_token,
#                     token_uri=user_credentials.token_uri,
#                     client_id=user_credentials.client_id,
#                     client_secret=user_credentials.client_secret,
#                     scopes=user_credentials.scopes.split(","),
#                 )

#                 return credentials

#             except requests.RequestException as e:
#                 return ValueError(f"RequestException: {str(e)}")
#             except Exception as e:
#                 return ValueError(f"Exception: {str(e)}")
            
#         # Create and return credentials
#         credentials = Credentials(
#             token=user_credentials.access_token,
#             refresh_token=user_credentials.refresh_token,
#             token_uri=user_credentials.token_uri,
#             client_id=user_credentials.client_id,
#             client_secret=user_credentials.client_secret,
#             scopes=user_credentials.scopes.split(","),
#         )
        
#         return credentials

#     else:
#         return ValueError("User credentials not found or refresh token missing.")
