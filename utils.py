from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from users.models import GoogleCredentials

def get_and_refresh_user_credentials(user):
    user_credentials = GoogleCredentials.objects.filter(user=user).first()

    if user_credentials and user_credentials.refresh_token:
        credentials = Credentials(
            token=user_credentials.access_token,
            refresh_token=user_credentials.refresh_token,
            token_uri=user_credentials.token_uri,
            client_id=user_credentials.client_id,
            client_secret=user_credentials.client_secret,
            scopes=user_credentials.scopes.split(',')
        )

        if credentials.expired:
            credentials.refresh(Request())
            # Обновление сохраненных токенов в базе данных
            user_credentials.access_token = credentials.token
            user_credentials.save()

        return credentials
        
    else:
        return ValueError("User credentials not found or refresh token missing.")