# Generated by Django 4.2.7 on 2024-07-16 12:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0006_alter_task_schedule_after"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="max_duration",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="min_duration",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="schedule_after",
            field=models.DateField(
                default=datetime.datetime(2024, 7, 16, 20, 3, 38, 743216), null=True
            ),
        ),
    ]