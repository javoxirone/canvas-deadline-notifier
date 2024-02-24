import asyncio
import logging
import sys
from datetime import datetime, timedelta

from aiogram.filters import Command
from aiogram.types import Message

from base import dp, bot, canvas
from tasks import notify_assignment_deadline, clear_schedule_queue


@dp.message(Command("start", ))
async def handle_start_command(message: Message) -> None:
    chat_id = message.from_user.id
    assignments = canvas.get_all_assignments()
    for assignment in assignments:
        eta = assignment["assignment_due_at"] - timedelta(days=1)
        eta.replace(hour=14, minute=0, second=0, microsecond=0)
        notify_assignment_deadline.apply_async((chat_id, assignment,), eta=eta)
    await message.answer("All deadlines are scheduled!")


@dp.message(Command('reset', ))
async def handle_reset_command(message: Message) -> None:
    clear_schedule_queue()
    await message.answer("Schedule queue is clean!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
