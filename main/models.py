from django.db import models
from django.db.models import UniqueConstraint


class Color(models.Model):
    color_id = models.CharField(max_length=4, null=True)
    name = models.CharField(max_length=255)
    hex = models.CharField(max_length=8)

    def __str__(self):
        return "%s (id %s)" % (self.name, self.pk)

    class Meta:
        db_table = "color"
        constraints = [
            UniqueConstraint(fields=["color_id"], name="unique_color_id"),
            UniqueConstraint(fields=["name"], name="unique_color_name"),
            UniqueConstraint(fields=["hex"], name="unique_color_hex"),
        ]