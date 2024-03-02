import subprocess
from typing import Dict
from database.models import User
from database.base import session
from config.integrations import notifier_bot

def send_notification(chat_id: int, data: Dict):
    notifier_bot.send_message(
        chat_id,
        f"<strong>Course name: </strong>{data['course_name']}\n"
        f"<strong>Assignment title: </strong>{data['assignment_name']}\n"
        f"<strong>Assignment deadline: </strong>{data['assignment_due_at']}",
    )


# Find other ways of clearing a queue
def clear_schedule_queue() -> None:
    subprocess.run("celery -A tasks purge -f", shell=True)


# Rewrite this function
def handle_days_word(days: int) -> str:
    if days == 1:
        return "day"
    return "day"


def user_exists(telegram_id) -> None:
    # Read sqlalchemy package docs on the internet
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
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
        new_user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            notify_before_days=1,
        )
        session.add(new_user)
        session.commit()
        session.close()


def set_token(telegram_id: int, token: str) -> None:
    """
    This service sets token to the user's record.

    :param telegram_id: Unique ID of the Telegram user.
    :param token: Unique TOKEN of the Canvas user (student).
    """
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    print(user)
    user.token = token
    session.commit()
    session.close()


def update_notify_days_before_field_of_single_user(
    telegram_id: int, days: int = 1
) -> None:
    """
    This service gets days as an argument and updates notify_days_before field of a user record on db.

    :param telegram_id: Unique identification of a user on telegram.
    :param days: (optional) Number of days before user should be notified.
    """
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    user.notify_before_days = days
    session.commit()
    session.close()


def get_notify_days_before_field_of_single_user(telegram_id: int) -> int:
    """
    This service returns notify_days_before field of single user record by getting telegram_id as an argument.

    :param telegram_id: Unique ID of a user on telegram.
    :return: notify_days_before field's value.
    """
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    return user.notify_before_days


def get_canvas_token_of_user(telegram_id: int) -> str:
    """
    This service gets canvas token of the user and returns it.

    :param telegram_id: Unique ID of the Telegram user.
    :return: Canvas Token of the user.
    """
    user = session.query(User).filter(User.telegram_id == telegram_id).first()
    canvas_token = user.token
    return canvas_token
