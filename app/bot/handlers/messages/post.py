from dataclasses import dataclass
from datetime import datetime

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hcode

from app.bot.handlers.windows.post import PostWindow
from app.bot.misc.messages import delete_message
from app.bot.misc.throttling import rate_limit, ThrottlingContext
from app.config import TIME_ZONE


@dataclass
class PostMessage:

    @staticmethod
    @rate_limit(1, "sleep")
    async def edit_time_handler(message: Message, state: FSMContext) -> None:
        def is_valid_time(string):
            try:
                datetime.strptime(string, '%d.%m.%Y %H:%M')
                return True
            except ValueError:
                return False

        match message:
            case message if message.text:
                async with ThrottlingContext(state):
                    if is_valid_time(message.text):
                        await state.update_data(new_time=message.text)
                        await PostWindow.edit_time_confirm(state, message=message)
                    else:
                        current_date = datetime.now(tz=pytz.timezone(TIME_ZONE)).strftime("%d.%m.%Y %H:%M")
                        text = (
                            "<b>Неверный формат даты и времени.</b>\n"
                            "<b>Допустимый формат:</b> <code>ДД.ММ.ГГГГ ЧЧ:ММ</code>\n\n"
                            f"<b>Пример:</b> <code>{current_date}</code>"
                        )
                        await PostWindow.edit_time(state, message=message, text=text)
            case _:
                await delete_message(message)

    @staticmethod
    @rate_limit(1, "sleep")
    async def edit_comment_handler(message: Message, state: FSMContext) -> None:
        match message:
            case message if message.text:
                async with ThrottlingContext(state):
                    text_limit = 2000
                    if len(message.text) <= text_limit:
                        await state.update_data(new_comment=message.text)
                        await PostWindow.edit_comment_confirm(state, message=message)
                    else:
                        text = (
                            f"<b>Комментарий не должен превышать {text_limit} символов.</b>\n\n"
                            f"Обрезанный текст до {text_limit} символов:\n"
                            f"{hcode(message.text[:text_limit])}"
                        )
                        await PostWindow.edit_comment(state, message=message, text=text)
            case _:
                await delete_message(message)
