from aiogram.types import Message
from services.services import (
    register_user,
    set_token,
    clear_schedule_queue,
    handle_days_word,
    update_notify_days_before_field_of_single_user,
    get_notify_days_before_field_of_single_user,
    get_canvas_token_of_user,
)
from tasks import schedule_all_deadlines_for_single_user
from bot.decorators.auth_decorators import (
    check_token,
    register_user,
)


@register_user
async def handle_start_command(message: Message) -> None:
    user = message.from_user
    await message.answer(
        f"Hello, {user.first_name} 👋\n"
        f"This is Canvas Deadlines Notifier bot.\n\n"
        f"You can schedule all notifications by just sending <strong>/schedule_deadlines</strong>\n\n"
        f"By default it will set notification 1 day before your deadline to all you assignments. You can modify this settings by sending <strong>/notify_days_before number_of_days</strong>"
    )


@register_user
async def handle_token_command(message: Message) -> None:
    user = message.from_user
    token = message.text.split(" ")[1]
    set_token(user.id, token)
    await message.answer("Your token is registered!\n" "Now, you can enjoy our bot!")
    await message.answer("Now, send /schedule_deadlines to schedule notifications!")


@register_user
async def handle_help_command(message: Message) -> None:
    await message.answer(
        "Commands available to use:\n\n"
        "/start - start the bot\n"
        "/help - list of commands to use\n"
        "/schedule_deadlines - schedules all deadlines of assignments days before\n"
        "/notify_days_before number_of_days - changes the number of days before deadlines should be scheduled\n"
        "/reset - clears out all scheduled notifications\n\n"
        "<i>Write to @abbos_shodiev or @javoxirone, if you have any questions.</i>"
    )


@check_token
@register_user
async def handle_schedule_deadlines_command(message: Message) -> None:
    clear_schedule_queue()
    user = message.from_user
    telegram_id = user.id
    notify_days_before = get_notify_days_before_field_of_single_user(telegram_id)
    user_canvas_token = get_canvas_token_of_user(telegram_id)
    schedule_all_deadlines_for_single_user.delay(
        user_canvas_token, telegram_id, notify_days_before
    )


@check_token
@register_user
async def handle_notify_days_before_command(message: Message) -> None:
    user = message.from_user
    telegram_id = user.id
    command_split = message.text.split(" ")
    if len(command_split) == 1:
        await message.answer(
            "Please send this command with days paramater!\n(e.g. <strong>/notify_days_before 3</strong>)"
        )
        return
    days = int(command_split[1])

    update_notify_days_before_field_of_single_user(telegram_id, days)
    notify_days_before = get_notify_days_before_field_of_single_user(telegram_id)
    clear_schedule_queue()
    user_canvas_token = get_canvas_token_of_user(telegram_id)
    schedule_all_deadlines_for_single_user.delay(
        user_canvas_token, telegram_id, notify_days_before
    )
    await message.answer(f"Notification time changed to {notify_days_before} days.")


@check_token
@register_user
async def handle_reset_command(message: Message) -> None:
    clear_schedule_queue()
    await message.answer("All scheduled notifications were removed!")
