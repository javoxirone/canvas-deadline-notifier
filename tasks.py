import subprocess
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from config.constants import REDIS_HOST
from services.services import clear_schedule_queue, send_notification
from api.canvas import CanvasAPI
from config.integrations import notifier_bot

app = Celery("tasks", broker=REDIS_HOST, backend=REDIS_HOST)

app.conf.timezone = "UTC"

app.conf.beat_schedule = {
    "refresh_all_deadlines_schedules": {
        "task": "tasks.refresh_schedules",
        # executing task every 24 hours
        "schedule": crontab(hour=0, minute=0),
    },
}


@app.task
def refresh_schedules(token: str):
    clear_schedule_queue()
    canvas = CanvasAPI(token)
    assignments = canvas.get_all_assignments()
    for assignment in assignments:
        eta = assignment["assignment_due_at"] - timedelta(days=1)
        eta.replace(hour=14, minute=0, second=0, microsecond=0)
        notify_assignment_deadline.apply_async(
            (
                957481488,
                assignment,
            ),
            eta=eta,
        )


@app.task
def notify_assignment_deadline(chat_id: int, data: dict) -> bool:
    send_notification(chat_id, data)
    print(data["assignment_name"], data["assignment_due_at"])


@app.task
def schedule_all_deadlines_for_single_user(token: str, chat_id: int, days: int = 1):
    try:
        canvas = CanvasAPI(token)
        assignments = canvas.get_all_assignments()
        for assignment in assignments:
            eta = assignment["assignment_due_at"] - timedelta(days=days)
            eta.replace(hour=14, minute=0, second=0, microsecond=0)
            notify_assignment_deadline.apply_async(
                (
                    chat_id,
                    assignment,
                ),
                eta=eta,
            )
        notifier_bot.send_message(chat_id, "All deadlines were scheduled successfully!")
    except Exception as e:
        notifier_bot.send_message(chat_id, "Something went wrong!")
