import pytz
from django.db import models
from datetime import datetime, timedelta
from users.models import CustomUser, Hours
from django.utils import timezone
from utils import Priority, PRIORITY_CHOICES

# Create your models here.
class Task(models.Model):

    name = models.CharField(max_length=255)
    priority = models.CharField(choices=PRIORITY_CHOICES, default=Priority.HIGH, max_length=20)
    duration = models.IntegerField(default=60)
    min_duration = models.IntegerField(default=None, null=True)
    max_duration = models.IntegerField(default=None, null=True)
    schedule_after = models.DateTimeField(default=datetime.now(), null=True)
    due_date = models.DateTimeField(default=datetime.now() + timedelta(days=3), blank=True)
    time_spent = models.DurationField(null=True, default=timedelta(minutes=0))
    private = models.BooleanField(default=True)
    visibility = models.CharField(
        max_length=200, default="Busy", null=True
    )  # Что показывается в календаре для других людей
    notes = models.TextField(blank=True)

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tasks", null=True
    )
    hours = models.ForeignKey(
        Hours, on_delete=models.SET_NULL, related_name="tasks", null=True, default=None
    )

    def to_json(self):
        taks_json = {
            "id": self.pk,
            "name": self.name,
            "priority": self.priority,
            "duration": self.duration,
            "min_duration": self.min_duration,
            "max_duration": self.max_duration,
            "schedule_after": self.schedule_after,
            "due_date": self.due_date,
            "private": self.private,
            "hours": {"id": self.hours.pk, "name": self.hours.name, "intervals": self.hours.intervals} if self.hours else None,
            "time_spent": self.time_spent,
        }
        return taks_json

    def get_hours(self):
        task_hours = Hours.objects.get(id=self.hours.pk)
        return task_hours.intervals

    def save(self, *args, **kwargs):
        user_timezone = pytz.timezone(self.user.time_zone)
        timezone.activate(user_timezone )
        # if not self.min_duration:
        #     self.min_duration = self.duration
        # if not self.max_duration:
        #     self.max_duration = self.duration
        if not self.schedule_after:
            self.schedule_after = timezone.now()
        if self.due_date < timezone.now():
            self.due_date = timezone.now()
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return "%s (id %s)" % (self.name, self.pk)

    class Meta:
        db_table = "task"
