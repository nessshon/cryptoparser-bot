from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType
from aiogram.utils.exceptions import ChatNotFound

from app.bot.handlers.windows.channel import ChannelWindow
from app.bot.misc.messages import delete_message
from app.bot.misc.throttling import rate_limit, ThrottlingContext
from app.db.sqlite.manage import Database


@dataclass
class ChannelMessage:

    @staticmethod
    @rate_limit(1, "sleep")
    async def add_channel_handler(message: Message, state: FSMContext) -> None:
        db: Database = message.bot.get("db")

        match message:
            case message if message.text or message.forward_from_chat:
                async with ThrottlingContext(state):
                    try:
                        chat_id = message.forward_from_chat.id if message.forward_from_chat else message.text
                        chat = await message.bot.get_chat(chat_id=chat_id)
                        if chat.type == ChatType.CHANNEL:
                            if await db.channel.is_exists(chat.id):
                                text = "<b>Канал уже существует.</b>"
                                await ChannelWindow.add_channel(state, message=message, text=text)
                            else:
                                await state.update_data(channel_id=chat.id, channel_title=chat.title)
                                await ChannelWindow.add_channel_choose_lang(state, message=message)
                        else:
                            text = "<b>Этот ID не принадлежит каналу, пришлите ID канала.</b>"
                            await ChannelWindow.add_channel(state, message=message, text=text)
                    except ChatNotFound:
                        text = "<b>Канал не найден. Убедитесь, что бот добавлен в канал в качестве администратора.</b>"
                        await ChannelWindow.add_channel(state, message=message, text=text)
            case _:
                await delete_message(message)

    @staticmethod
    @rate_limit(1, "sleep")
    async def edit_title_handler(message: Message, state: FSMContext) -> None:
        match message:
            case message if message.text:
                async with ThrottlingContext(state):
                    if len(message.text) <= 256:
                        await state.update_data(new_channel_title=message.text)
                        await ChannelWindow.edit_title_confirm(state, message=message)
                    else:
                        text = "<b>Название канала не должно превышать 256 символов.</b>"
                        await ChannelWindow.edit_title(state, message=message, text=text)
            case _:
                await delete_message(message)
