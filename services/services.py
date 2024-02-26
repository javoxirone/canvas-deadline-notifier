import subprocess
from typing import Dict
from database.models import User
from database.base import session

def send_notification(chat_id: int, data: Dict):
    from bot.bot import notifier_bot
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

def user_exists(telegram_id) -> None:
    user = session.query(User).filter(telegram_id == telegram_id).first()
    print(user)
    return user is not None
    

def register_user(user) -> None:
    """
    This service gets user object as an argument and checks if the user exists. If there is no such user it will create new one.

    :param user: User object.
    """
    telegram_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    if not user_exists(telegram_id):
        new_user = User(telegram_id=telegram_id, first_name=first_name, last_name=last_name, username=username)
        session.add(new_user)
        session.commit()