import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST')
CANVAS_API_TOKEN = os.getenv('CANVAS_API_TOKEN')
