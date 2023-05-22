from contextlib import suppress

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, User


async def delete_message(message: Message) -> None:
    with suppress(Exception):
        await message.delete()


async def delete_previous_message(bot: Bot, state: FSMContext) -> None:
    user = User.get_current()
    data = await state.get_data()

    with suppress(Exception):
        message_id = data["message_id"]
        await bot.delete_message(
            chat_id=user.id, message_id=message_id
        )
