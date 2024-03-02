from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from bot.handlers.command_handlers import *
from config.constants import TOKEN


bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# Registering command handlers
dp.message.register(
    handle_start_command,
    Command(
        "start",
    ),
)
dp.message.register(
    handle_token_command,
    Command(
        "token",
    ),
)
dp.message.register(
    handle_notify_days_before_command,
    Command(
        "notify_days_before",
    ),
)
dp.message.register(
    handle_reset_command,
    Command(
        "reset",
    ),
)
dp.message.register(
    handle_schedule_deadlines_command,
    Command(
        "schedule_deadlines",
    ),
)
dp.message.register(
    handle_help_command,
    Command(
        "help",
    ),
)
