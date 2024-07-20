from .models import Hours

CUSTOM_WORK_INTERVALS = {"Monday": [{"start": "9:00", "end": "18:00"}], 
                    "Tuesday": [{"start": "9:00", "end": "18:00"}], 
                    "Wednesday": [{"start": "9:00", "end": "18:00"}], 
                    "Thursday": [{"start": "9:00", "end": "18:00"}], 
                    "Friday": [{"start": "9:00", "end": "18:00"}]}

CUSTOM_PERSONAL_INTERVALS = {"Monday": [{"start": "18:00", "end": "22:00"}], 
                    "Tuesday": [{"start": "18:00", "end": "22:00"}], 
                    "Wednesday": [{"start": "18:00", "end": "22:00"}], 
                    "Thursday": [{"start": "18:00", "end": "22:00"}], 
                    "Friday": [{"start": "18:00", "end": "22:00"}], 
                    "Saturday": [{"start": "9:00", "end": "22:00"}], 
                    "Sunday": [{"start": "9:00", "end": "22:00"}]}


def get_hours_by_id(id):
    '''Returns Hours object by primary key (id)'''
    return Hours.objects.get(id=id)


def create_user_custom_hours(user):
    '''Creates default hours for created user, calendar set to Primary'''
    personal_hours = Hours.objects.filter(user=user, name="Personal Hours").first()
    work_hours = Hours.objects.filter(user=user, name="Work Hours").first()
    try:
        primary_calendar = user.get_primary_calendar()
        if not work_hours:
            work_hours = Hours.objects.create(user=user, name="Work Hours", calendar=primary_calendar, intervals=CUSTOM_WORK_INTERVALS)
        if not personal_hours:
            personal_hours = Hours.objects.create(user=user, name="Personal Hours", calendar=primary_calendar, intervals=CUSTOM_PERSONAL_INTERVALS)
        return [personal_hours.to_json(), work_hours.to_json()]
    except Exception as e:
        raise ValueError(f"Error: {e}")
    

def set_user_timezone_from_primary_calendar(user):
    try:
        primary_calendar = user.get_primary_calendar()
        user_timezone = primary_calendar["timeZone"]
        user.time_zone = user_timezone
        user.save()
        return True
    except Exception as e:
        return False