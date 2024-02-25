import asyncio
import logging
import sys

from aiogram.filters import Command
from aiogram.types import Message

from base import dp, bot, canvas
from tasks import clear_schedule_queue, schedule_all_deadlines_for_single_user
from services import handle_days_word

@dp.message(Command("start", ))
async def handle_start_command(message: Message) -> None:
    chat_id = message.from_user.id
    schedule_all_deadlines_for_single_user.delay(chat_id)
    await message.answer("All deadlines are scheduled!")

@dp.message(Command("notify_days_before", ))
async def handle_notify_days_before_command(message: Message) -> None:
    chat_id = message.from_user.id
    days = int(message.text.split(" ")[1])
    print(days)
    clear_schedule_queue()
    schedule_all_deadlines_for_single_user.delay(chat_id, days)
    await message.answer(f"Notification will come {days} {handle_days_word(days)} before the deadline!")


@dp.message(Command('reset', ))
async def handle_reset_command(message: Message) -> None:
    clear_schedule_queue()
    await message.answer("Schedule queue is clean!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
