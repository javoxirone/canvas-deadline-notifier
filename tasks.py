import subprocess
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from base import canvas, redis_host
from services import clear_schedule_queue, send_notification
app = Celery('tasks', broker=redis_host,
             backend=redis_host)

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'refresh_all_deadlines_schedules': {
        'task': 'tasks.refresh_schedules',
        # executing task every 24 hours
        'schedule': crontab(hour=0, minute=0),
    },
}


@app.task
def refresh_schedules():
    clear_schedule_queue()
    assignments = canvas.get_all_assignments()
    for assignment in assignments:
        eta = assignment["assignment_due_at"] - timedelta(days=1)
        eta.replace(hour=14, minute=0, second=0, microsecond=0)
        notify_assignment_deadline.apply_async((957481488, assignment,), eta=eta)


@app.task
def notify_assignment_deadline(chat_id: int, data):
    send_notification(chat_id, data)
    print(data["assignment_name"], data["assignment_due_at"])

@app.task
def schedule_all_deadlines_for_single_user(chat_id: int, days:int=1):
    assignments = canvas.get_all_assignments()
    for assignment in assignments:
        eta = assignment["assignment_due_at"] - timedelta(days=days)
        eta.replace(hour=14, minute=0, second=0, microsecond=0)
        notify_assignment_deadline.apply_async((chat_id, assignment,), eta=eta)