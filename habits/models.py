from django.db import models
from datetime import time, date

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
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES, default=('high', 'High'))
    min_duration = models.IntegerField(default=30) # Длительность в минутах
    max_duration = models.IntegerField(default=60)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=('personal', 'Personal'))
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default=('weekly', 'Weekly'))
    times_per_period = models.SmallIntegerField(default=1)
    # schedule = models.JSONField(verbose_name='period & times per period', default=DEFAULT_SCHEDULE) # Расписание в виде {'period': 'weekly', 'times': '3'}
    ideal_days = models.JSONField(blank=True, null=True)
    ideal_time = models.TimeField(default=time(8, 0))
    starting = models.DateField(default=date.today) # Дата начала 
    ending = models.DateField(blank=True, null=True) # Дата окончания
    # private = models.BooleanField(default=True) # Приватность отображения в календаре для других
    visibility = models.CharField(max_length=200, default='Busy') # Что показывается в календаре для других людей
    notes = models.TextField(blank=True)
    
    # hours_category = 
    # hours = 

    def __str__(self):
        return "%s (id %s)" % (self.name, self.pk)

    class Meta:
        db_table = "habit"
