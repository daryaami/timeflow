# Generated by Django 4.2.7 on 2024-07-14 13:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="time_spent",
            field=models.DurationField(default=datetime.timedelta(0), null=True),
        ),
    ]