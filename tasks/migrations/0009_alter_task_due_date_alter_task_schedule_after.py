# Generated by Django 4.2.7 on 2024-07-16 13:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0008_alter_task_priority_alter_task_schedule_after"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="due_date",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime(2024, 7, 19, 21, 42, 16, 133221)
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="schedule_after",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 7, 16, 21, 42, 16, 133221), null=True
            ),
        ),
    ]