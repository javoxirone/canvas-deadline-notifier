from api.canvas import CanvasAPI
from telebot import telebot
from config.constants import CANVAS_API_TOKEN, TOKEN

canvas = CanvasAPI(CANVAS_API_TOKEN)
notifier_bot = telebot.TeleBot(TOKEN, parse_mode="HTML")