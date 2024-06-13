from django.db import models


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=120, unique=True)
    duration = models.JSONField() 
    schedule = models.JSONField()
    ideal_time = models.TimeField(blank=True, null=True)
    private = models.BooleanField(default=True)

    def __str__(self):
        return "%s (id %s)" % (self.name, self.pk)

    class Meta:
        db_table = "task"