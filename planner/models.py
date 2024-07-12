from django.db import models


# Create your models here.
# class Hours(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='hours')
#     calendar = models.ForeignKey(UserCalendar, on_delete=models.SET_NULL, related_name='hours', null=True, default=None)

#     name = models.CharField(max_length=255)
#     intervals = models.JSONField()  # Пример: {"Monday": [{"start": "12:00", "end": "14:00"}, {"start": "16:00", "end": "18:00"}], "Wednesday": [{"start": "13:00", "end": "19:00"}]}

#     def __str__(self):
#         return "%s (id %s)" % (self.name, self.pk)

#     class Meta:
#         db_table = "hours"