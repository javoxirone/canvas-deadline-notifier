import os
import telebot
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from canvas import CanvasAPI

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
notifier_bot = telebot.TeleBot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
redis_host = os.getenv('REDIS_HOST')
canvas = CanvasAPI(os.getenv('CANVAS_API_TOKEN'))
