from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import Command
from api.canvas import CanvasAPI
from bot.handlers.command_handlers import *
from config.constants import TOKEN, CANVAS_API_TOKEN



bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# Registering handlers
dp.message.register(handle_start_command, Command("start", ))
dp.message.register(handle_notify_days_before_command, Command("notify_days_before", ))
dp.message.register(handle_reset_command, Command('reset', ))
