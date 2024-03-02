from database.base import session
from database.models import User
from services.services import user_exists, get_canvas_token_of_user
from aiogram import Bot
from aiogram.enums import ParseMode
from config.constants import TOKEN

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


def check_token(func):
    async def wrapper(message):
        user = message.from_user
        telegram_id = user.id
        if not get_canvas_token_of_user(telegram_id):
            await bot.send_message(
                telegram_id,
                "<strong>WARNING: Please set Canvas Token to get notifications!</strong>\n\n"
                "Use command below to set Canvas token:\n"
                "/token your_cavnas_token",
            )
        await func(message)

    return wrapper


def register_user(func):
    async def wrapper(message):
        try:
            user = message.from_user
            telegram_id = user.id
            first_name = user.first_name
            last_name = user.last_name
            username = user.username
            new_user = User(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                notify_before_days=1,
            )
            session.add(new_user)
            session.commit()
        except Exception as e:
            print(e)
        finally:
            session.close()
        await func(message)

    return wrapper
