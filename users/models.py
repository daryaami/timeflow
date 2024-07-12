from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from google.oauth2.credentials import Credentials
from django.db import models
import requests
from django.utils import timezone
from datetime import datetime, timedelta
from app import settings


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, name, password=None, image=None, time_zone=None, **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, image=image, time_zone=time_zone, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, name, password, image=None, time_zone=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, name, password, image, time_zone, **extra_fields)

    # from users.models import CustomUser
    # CustomUser.objects.create_superuser(email='admin@example.com', name='Admin', password='adminpassword')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    image = models.URLField(blank=True, null=True)
    joined_on = models.DateField(default=datetime.today)
    time_zone = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def get_and_refresh_credentials(self):
        user_credentials = GoogleCredentials.objects.filter(user=self).first()

        if not user_credentials:
            return ValueError("User credentials not found.")
        
        if user_credentials.refresh_token:
            if user_credentials.access_token_expiry < timezone.now():
                try:
                # Refresh the access token
                    refresh_request = requests.post(
                            settings.TOKEN_URI,
                            data={
                                "client_id": user_credentials.client_id,
                                "client_secret": user_credentials.client_secret,
                                "refresh_token": user_credentials.refresh_token,
                                "grant_type": "refresh_token",
                            },
                        )
                    
                    if refresh_request.status_code != 200:
                        return ValueError(f"Failed to refresh token: {refresh_request.status_code}, {refresh_request.text}")

                    new_credentials = refresh_request.json()

                    user_credentials.access_token = new_credentials.get("access_token")
                    user_credentials.access_token_expiry = timezone.now() + timedelta(seconds=new_credentials["expires_in"])
                    user_credentials.save()

                    credentials = Credentials(
                        token=user_credentials.access_token,
                        refresh_token=user_credentials.refresh_token,
                        token_uri=user_credentials.token_uri,
                        client_id=user_credentials.client_id,
                        client_secret=user_credentials.client_secret,
                        scopes=user_credentials.scopes.split(","),
                    )

                    return credentials

                except requests.RequestException as e:
                    return ValueError(f"RequestException: {str(e)}")
                except Exception as e:
                    return ValueError(f"Exception: {str(e)}")
                
            # Create and return credentials
            credentials = Credentials(
                token=user_credentials.access_token,
                refresh_token=user_credentials.refresh_token,
                token_uri=user_credentials.token_uri,
                client_id=user_credentials.client_id,
                client_secret=user_credentials.client_secret,
                scopes=user_credentials.scopes.split(","),
            )
            
            return credentials

        else:
            return ValueError("User credentials not found or refresh token missing.")

    def get_calendars(self):
        return UserCalendar.objects.filter(user=self)

    class Meta:
        db_table = "user"


class GoogleCredentials(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_uri = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    scopes = models.CharField(max_length=255)
    access_token_expiry = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s (id %s)" % (self.user.email, self.pk)

    class Meta:
        db_table = "user_credentials"


class UserCalendar(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)

    class Meta:
        db_table = "user_calendars"

    def __str__(self):
        return "%s (id %s)" % (self.summary, self.pk)


class Hours(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="hours")
    calendar = models.ForeignKey(
        UserCalendar,
        on_delete=models.SET_NULL,
        related_name="hours",
        null=True,
        default=None,
    )
    name = models.CharField(max_length=255)
    intervals = (
        models.JSONField()
    )  # Пример: {"Monday": [{"start": "12:00", "end": "14:00"}, {"start": "16:00", "end": "18:00"}], "Wednesday": [{"start": "13:00", "end": "19:00"}]}

    def __str__(self):
        return "%s (id %s)" % (self.name, self.pk)

    class Meta:
        db_table = "hours"
