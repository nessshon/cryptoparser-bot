from dataclasses import dataclass
from datetime import datetime

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hcode

from app.bot.handlers.windows.token import TokenWindow
from app.bot.misc.messages import delete_message
from app.bot.misc.throttling import rate_limit, ThrottlingContext
from app.db.mysql.manage import Database


@dataclass
class TokenMessage:

    @staticmethod
    @rate_limit(1, "sleep")
    async def create_post_handler(message: Message, state: FSMContext) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db")

        match message:
            case message if message.text:
                async with ThrottlingContext(state):
                    text_limit = 2000
                    if len(message.text) <= text_limit:
                        await db.token.update(id_=data["token_id"], comment=message.text)
                        await TokenWindow.choose_channel(state, message=message)
                    else:
                        text = (
                            f"<b>Комментарий не должен превышать {text_limit} символов.</b>\n\n"
                            f"Обрезанный текст до {text_limit} символов:\n"
                            f"{hcode(message.text[:text_limit])}"
                        )
                        await TokenWindow.create_post(state, message=message, text=text)
            case _:
                await delete_message(message)

    @staticmethod
    @rate_limit(1, "sleep")
    async def send_time_handler(message: Message, state: FSMContext) -> None:
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
                        await state.update_data(time=message.text)
                        await TokenWindow.create_postpone_confirm(state, message=message)
                    else:
                        current_date = datetime.now(tz=pytz.timezone("Europe/Moscow")).strftime("%d.%m.%Y %H:%M")

                        text = (
                            "<b>Неверный формат даты и времени.</b>\n"
                            "Допустимый формат: <code>ДД.ММ.ГГГГ ЧЧ:ММ</code>\n\n"
                            f"Пример: <code>{current_date}</code>"
                        )
                        await TokenWindow.send_time(state, message=message, text=text)
            case _:
                await delete_message(message)
