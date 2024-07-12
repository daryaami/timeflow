from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
import json
from datetime import datetime


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, image=None, time_zone=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, name=name, image=image, time_zone=time_zone, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, image=None, time_zone=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email, name, password, image, time_zone, **extra_fields
        )
    # from users.models import CustomUser
    # CustomUser.objects.create_superuser(email='admin@example.com', name='Admin', password='adminpassword')


# Create your models here.
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
    
    def get_name(self):
        return self.name

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='hours')
    calendar = models.ForeignKey(UserCalendar, on_delete=models.SET_NULL, related_name='hours', null=True, default=None)

    name = models.CharField(max_length=255)
    intervals = models.JSONField()  # Пример: {"Monday": [{"start": "12:00", "end": "14:00"}, {"start": "16:00", "end": "18:00"}], "Wednesday": [{"start": "13:00", "end": "19:00"}]}

    def __str__(self):
        return "%s (id %s)" % (self.name, self.pk)

    class Meta:
        db_table = "hours"