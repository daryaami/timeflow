from django.db import models
from django.db.models import UniqueConstraint


class Color(models.Model):
    color_id = models.CharField(max_length=4, null=True)
    name = models.CharField(max_length=255)
    background_color = models.CharField(max_length=8)
    foreground_color = models.CharField(max_length=8, default="#FFFFFF")

    def to_json(self):
        color_json = {
            "id": self.color_id,
            "name": self.name,
            "background_color": self.background_color,
            "foreground_color": self.foreground_color
        }
        return color_json

    def __str__(self):
        return "%s (id %s)" % (self.name, self.pk)

    class Meta:
        db_table = "color"
        constraints = [
            UniqueConstraint(fields=["color_id"], name="unique_color_id"),
            UniqueConstraint(fields=["name"], name="unique_color_name"),
            UniqueConstraint(fields=["background_color"], name="unique_color_hex"),
        ]