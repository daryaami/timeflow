from django.db import models
from datetime import time, date
from users.models import CustomUser

# Create your models here.
class Habit(models.Model):

    CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work')
    ]
    
    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]

    PERIOD_CHOICES = [
        ('every day', 'Every day'), 
        ('weekly', 'Weekly'), 
        ('monthly', 'Monthly')
    ]

    # DEFAULT_SCHEDULE = {"period": ('weekly', 'Weekly'), "times": "1"}

    name = models.CharField(max_length=255)
    priority = models.CharField(choices=PRIORITY_CHOICES, default='high', max_length=20)
    min_duration = models.IntegerField(default=30) # Длительность в минутах
    max_duration = models.IntegerField(default=60)
    category = models.CharField(choices=CATEGORY_CHOICES, default='personal', max_length=20)
    period = models.CharField(choices=PERIOD_CHOICES, default='weekly', max_length=20)
    times_per_period = models.SmallIntegerField(default=1)
    ideal_days = models.JSONField(blank=True, null=True)
    ideal_time = models.TimeField(default=time(8, 0))
    starting = models.DateField(default=date.today) # Дата начала 
    ending = models.DateField(blank=True, null=True) # Дата окончания
    # private = models.BooleanField(default=True) # Приватность отображения в календаре для других
    visibility = models.CharField(max_length=200, default='Busy') # Что показывается в календаре для других людей
    notes = models.TextField(blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='habits', null=True)
    
    # hours_category = 
    # hours = 

    def __str__(self):
        return "%s (id %s)" % (self.name, self.pk)

    class Meta:
        db_table = "habit"
