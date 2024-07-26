from enum import Enum

class Priority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Period(Enum):
    EVERYDAY = 'every day'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

PRIORITY_CHOICES = [
        (Priority.LOW.value, 'Low'),
        (Priority.MEDIUM.value, 'Medium'),
        (Priority.HIGH.value, 'High'),
        (Priority.CRITICAL.value, 'Critical'),
    ]

CATEGORY_CHOICES = [
        ('personal', 'Personal'),
        ('work', 'Work')
    ]

PERIOD_CHOICES = [
        ('every day', 'Every day'), 
        ('weekly', 'Weekly'), 
        ('monthly', 'Monthly')
    ]