# Generated by Django 4.2.7 on 2024-06-25 11:42

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("planner", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("critical", "Critical"),
                            ("high", "High"),
                            ("medium", "Medium"),
                            ("low", "Low"),
                        ],
                        default="high",
                        max_length=20,
                    ),
                ),
                ("time_needed", models.IntegerField(default=60)),
                ("min_duration", models.IntegerField(default=0)),
                ("max_duration", models.IntegerField(default=0)),
                ("due_date", models.DateField(blank=True)),
                ("schedule_after", models.DateField(default=datetime.date.today)),
                ("visibility", models.CharField(default="Busy", max_length=200)),
                ("notes", models.TextField(blank=True)),
                (
                    "hours",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tasks",
                        to="planner.hours",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "task",
            },
        ),
    ]
