
from .models import Color

def get_events_colors_json():
    colors = [color.to_json() for color in Color.objects()]
    return {"events_colors": colors}
