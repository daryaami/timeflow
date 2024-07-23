
from .models import Color

def get_events_colors_json():
    colors = [color.to_json() for color in Color.objects()]
    return {"events_colors": colors}

def get_event_color_hex(color_id):
    try:
        return Color.objects.get(color_id=int(color_id)).hex
    except Color.DoesNotExist:
        raise ValueError("Color does not exist.")
    except Exception as e:
        raise ValueError(f"Could not get event color hex: {e}")