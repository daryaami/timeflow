# Generated by Django 4.2.7 on 2024-06-20 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_usercalendar_googlecredentials"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="credentials",
        ),
    ]