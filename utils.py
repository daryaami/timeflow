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

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def calculate_luminance(rgb):
    r, g, b = [x/255.0 for x in rgb]
    r = r/12.92 if r <= 0.03928 else ((r+0.055)/1.055) ** 2.4
    g = g/12.92 if g <= 0.03928 else ((g+0.055)/1.055) ** 2.4
    b = b/12.92 if b <= 0.03928 else ((b+0.055)/1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def get_text_color(hex_color):
    rgb = hex_to_rgb(hex_color)
    luminance = calculate_luminance(rgb)
    return "#363945" if luminance > 0.6 else "#FFFFFF"