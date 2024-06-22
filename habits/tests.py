from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from users.models import CustomUser  # Подставьте правильный импорт
from .models import Habit
import json
from datetime import date, time

class AddHabitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', name='Test User', password='12345')
        self.client.login(email='testuser@example.com', password='12345')
        self.url = reverse('habits:add_habit')  # Убедитесь, что имя URL соответствует вашему маршруту

    def test_add_habit(self):
        data = {
            "name": "New Habit",
            "priority": "high",
            "min_duration": 30,
            "max_duration": 60,
            "category": "personal",
            "period": "weekly",
            "times_per_period": 1,
            "ideal_days": [],
            "ideal_time": "08:00",
            "starting": str(date.today()),
            "ending": None,
            "visibility": "Busy",
            "notes": "Some notes"
        }
        
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        
        # Проверка успешного ответа
        self.assertEqual(response.status_code, 201)
        
        # Проверка данных в ответе
        response_data = response.json()
        self.assertIn('habit', response_data)
        self.assertEqual(response_data['habit']['name'], data['name'])
        
        # Проверка, что привычка создана в базе данных
        habit = Habit.objects.get(name=data['name'])
        self.assertEqual(habit.priority, data['priority'])
        self.assertEqual(habit.min_duration, data['min_duration'])
        self.assertEqual(habit.max_duration, data['max_duration'])
        self.assertEqual(habit.category, data['category'])
        self.assertEqual(habit.period, data['period'])
        self.assertEqual(habit.times_per_period, data['times_per_period'])
        self.assertEqual(habit.ideal_time, time(8, 0))
        self.assertEqual(habit.starting, date.today())
        self.assertEqual(habit.visibility, data['visibility'])
        self.assertEqual(habit.notes, data['notes'])
        self.assertEqual(habit.user, self.user)
        
    def test_add_habit_missing_name(self):
        data = {
            "priority": "high",
            "min_duration": 30,
            "max_duration": 60,
            "category": "personal",
            "period": "weekly",
            "times_per_period": 1,
            "ideal_days": [],
            "ideal_time": "08:00",
            "starting": str(date.today()),
            "ending": None,
            "visibility": "Busy",
            "notes": "Some notes"
        }
        
        response = self.client.post(self.url, data=json.dumps(data), content_type='application/json')
        
        # Проверка ответа с ошибкой
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "Name is required")