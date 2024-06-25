from django.db import models
from datetime import date, timedelta
from users.models import CustomUser, UserCalendar
from planner.models import Hours


# Create your models here.
class Task(models.Model):

    PRIORITY_CHOICES = [
        ("critical", "Critical"),
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    name = models.CharField(max_length=255)
    priority = models.CharField(choices=PRIORITY_CHOICES, default="high", max_length=20)
    time_needed = models.IntegerField(default=60)
    min_duration = models.IntegerField(default=0)
    max_duration = models.IntegerField(default=0)
    due_date = models.DateField(blank=True)
    schedule_after = models.DateField(default=date.today)
    # private = models.BooleanField(default=True)
    visibility = models.CharField(max_length=200, default="Busy")  # Что показывается в календаре для других людей
    notes = models.TextField(blank=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks', null=True)
    hours = models.ForeignKey(Hours, on_delete=models.SET_NULL, related_name='tasks', null=True, default=None)

    def __str__(self):
        return "%s (id %s)" % (self.name, self.pk)

    def save(self, *args, **kwargs):
        if not self.min_duration:
            self.min_duration = self.time_needed
        if not self.max_duration:
            self.max_duration = self.time_needed
        super(Task, self).save(*args, **kwargs)

    class Meta:
        db_table = "task"
