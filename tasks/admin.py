from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')
    ordering = ('priority',)  # Сортировка по возрастанию

admin.site.register(Task)
