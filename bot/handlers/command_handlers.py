from aiogram.types import Message
from services.services import (
    register_user,
    clear_schedule_queue,
    handle_days_word,
    update_notify_days_before_field_of_single_user,
    get_notify_days_before_field_of_single_user
)
from tasks import schedule_all_deadlines_for_single_user

async def handle_start_command(message: Message) -> None:
    user = message.from_user
    register_user(user)
    await message.answer(f"Hello, {user.first_name} 👋\n"
                         f"This is Canvas Deadlines Notifier bot.\n\n"
                         f"You can schedule all notifications by just sending <strong>/schedule_deadlines</strong>\n\n"
                         f"By default it will set notification 1 day before your deadline to all you assignments. You can modify this settings by sending <strong>/notify_days_before number_of_days</strong>")
    
async def handle_help_command(message: Message) -> None:
    user = message.from_user
    register_user(user)
    await message.answer("Commands available to use:\n\n"
                         "/start - start the bot\n"
                         "/help - list of commands to use\n"
                         "/schedule_deadlines - schedules all deadlines of assignments days before\n"
                         "/notify_days_before number_of_days - changes the number of days before deadlines should be scheduled\n"
                         "/reset - clears out all scheduled notifications\n\n"
                         "<i>Write to @abbos_shodiev or @javoxirone, if you have any questions.</i>")

async def handle_schedule_deadlines_command(message: Message) -> None:
    clear_schedule_queue()
    user = message.from_user
    register_user(user)
    telegram_id = user.id
    notify_days_before = get_notify_days_before_field_of_single_user(telegram_id)
    result = schedule_all_deadlines_for_single_user.delay(telegram_id, notify_days_before)
    if result.status == "PENDING" or result.status == "SUCCESS":
        await message.answer("All deadlines were scheduled successfully!")
        return
    await message.answer("Something went wrong while scheduling deadlines!")



async def handle_notify_days_before_command(message: Message) -> None:
    user = message.from_user
    register_user(user)
    telegram_id = user.id
    command_split = message.text.split(" ")
    if len(command_split) == 1:
        await message.answer("Please send this command with days paramater!\n(e.g. <strong>/notify_days_before 3</strong>)")
        return
    days = int(command_split[1])
    
    update_notify_days_before_field_of_single_user(telegram_id, days)
    notify_days_before = get_notify_days_before_field_of_single_user(telegram_id)
    clear_schedule_queue()
    schedule_all_deadlines_for_single_user.delay(telegram_id, notify_days_before)
    await message.answer(f"Notification will come {notify_days_before} {handle_days_word(notify_days_before)} before the deadline!")


async def handle_reset_command(message: Message) -> None:
    user = message.from_user
    register_user(user)
    clear_schedule_queue()
    await message.answer("All scheduled notifications were removed!")
    