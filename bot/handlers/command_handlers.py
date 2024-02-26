from aiogram.types import Message
from services.services import register_user, clear_schedule_queue, handle_days_word
from tasks import schedule_all_deadlines_for_single_user

async def handle_start_command(message: Message) -> None:
    user = message.from_user
    register_user(user)
    chat_id = user.id
    schedule_all_deadlines_for_single_user.delay(chat_id)
    await message.answer("All deadlines are scheduled!")

async def handle_notify_days_before_command(message: Message) -> None:
    user = message.from_user
    register_user(user)
    chat_id = user.id
    days = int(message.text.split(" ")[1])
    print(days)
    clear_schedule_queue()
    schedule_all_deadlines_for_single_user.delay(chat_id, days)
    await message.answer(f"Notification will come {days} {handle_days_word(days)} before the deadline!")


async def handle_reset_command(message: Message) -> None:
    user = message.from_user
    register_user(user)
    clear_schedule_queue()
    await message.answer("Schedule queue is clean!")

