import subprocess
from base import notifier_bot
from typing import Dict

def send_notification(chat_id: int, data: Dict):
    notifier_bot.send_message(chat_id, f"<strong>Course name: </strong>{data['course_name']}\n"
                                       f"<strong>Assignment title: </strong>{data['assignment_name']}\n"
                                       f"<strong>Assignment deadline: </strong>{data['assignment_due_at']}")

# Find other ways of clearing a queue
def clear_schedule_queue() -> None:
    subprocess.run("celery -A tasks purge -f", shell=True)


# Rewrite this function
def handle_days_word(days: int) -> str:
    if days == 1:
        return "day"
    return "day"