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

class ColorEnum(Enum):
    TOMATO = "#D04747"     # Red
    FLAMINGO = "#D98282"      # Light Red
    TANGERINE = "#E07F49"  # Orange
    BANANA = "#FCE56D"   # Yellow
    SAGE = "#8BE1AD"       # Green
    BASIL = "#2B985D"    # Dark Green
    PEACOCK = "#198EBC"   # Light Blue
    BLUEBERRY = "#0E5F8D"      # Blue
    LAVENDER = "#9F80E0"   # Purple
    GRAPE = "#9F54AB"      # Dark Purple
    GRAPHITE = "#595E61"      # Gray
    CALENDAR_COLOR = None

id_to_color = {
    '1': ColorEnum.LAVENDER,
    '2': ColorEnum.SAGE,
    '3': ColorEnum.GRAPE,
    '4': ColorEnum.FLAMINGO,
    '5': ColorEnum.BANANA,
    '6': ColorEnum.TANGERINE,
    '7': ColorEnum.PEACOCK,
    '8': ColorEnum.GRAPHITE,
    '9': ColorEnum.BLUEBERRY,
    '10': ColorEnum.BASIL,
    '11': ColorEnum.TOMATO,
    None: ColorEnum.CALENDAR_COLOR
}

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


# colors = [
#     "#D04747", 
#     "#D98282", 
#     "#E07F49", 
#     "#FCE56D",
#     "#8BE1AD", 
#     "#2B985D", 
#     "#198EBC", 
#     "#0E5F8D",
#     "#9F80E0", 
#     "#9F54AB", 
#     "#595E61",
# ]
# text_colors = {color: get_text_color(color) for color in colors}
# print(text_colors)

from main.models import Color
def create_colors():
    try:
        for id in id_to_color:
            Color.objects.update_or_create(color_id=id, name=id_to_color[id].name, hex=id_to_color[id].value)
        return True
    except Exception as e:
        raise ValueError("Could not create colors.")