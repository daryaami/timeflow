from .models import Task


def get_user_tasks(user):
    user_tasks = Task.objects.filter(user=user)
    return [task.to_json() for task in user_tasks] 


def create_new_user_task(user, **params):
    try:
        task = Task.objects.create(name=params['name'], 
                            priority=params['priority'], 
                            duration=params["duration"], 
                            min_duration=params['min_duration'], 
                            max_duration=params['max_duration'],
                            schedule_after=params['schedule_after'],
                            due_date=params['due_date'],
                            hours=params['hours'],
                            user=user,
                            private=params['private'],
                            color=params['color']
                            )
        return task
    except Exception as e:
        raise ValueError(f"Failed to create a new task: Exception {e}")
