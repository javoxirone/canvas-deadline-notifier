import subprocess
import asyncio
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from base import bot, canvas, redis_host

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


async def send_awaited_message(chat_id, data):
    await bot.send_message(chat_id, f"<strong>Course name: </strong>{data['course_name']}\n"
                                    f"<strong>Assignment title: </strong>{data['assignment_name']}\n"
                                    f"<strong>Assignment deadline: </strong>{data['assignment_due_at']}")


def clear_schedule_queue():
    subprocess.run("celery -A tasks purge -f", shell=True)


@app.task
def refresh_schedules():
    clear_schedule_queue()
    assignments = canvas.get_all_assignments()
    for assignment in assignments:
        eta = assignment["assignment_due_at"] - timedelta(days=1)
        eta.replace(hour=14, minute=0, second=0, microsecond=0)
        notify_assignment_deadline.apply_async((957481488, assignment,), eta=eta)


@app.task
def notify_assignment_deadline(chat_id, data):
    asyncio.run(send_awaited_message(chat_id, data))
