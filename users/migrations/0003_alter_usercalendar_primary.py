# Generated by Django 4.2.7 on 2024-07-16 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_usercalendar_primary"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercalendar",
            name="primary",
            field=models.BooleanField(default=False),
        ),
    ]
