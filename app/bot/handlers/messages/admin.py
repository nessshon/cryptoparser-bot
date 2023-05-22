from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.bot.handlers.windows.admin import AdminWindow
from app.bot.misc.messages import delete_message
from app.bot.misc.throttling import rate_limit, ThrottlingContext
from app.db.sqlite.manage import Database


@dataclass
class AdminMessage:

    @staticmethod
    @rate_limit(1, "sleep")
    async def add_admin_handler(message: Message, state: FSMContext) -> None:
        db: Database = message.bot.get("db")

        match message:
            case message if message.text or message.forward_from:
                async with ThrottlingContext(state):
                    if message.text.isdigit() or message.forward_from:
                        user_id = int(message.forward_from.id) if message.forward_from else int(message.text)
                        if not user_id:
                            text = "<b>Пользователь не найден. Возможно он скрыл свой ID.</b>"
                            await AdminWindow.add_admin(state, message=message, text=text)
                        else:
                            if await db.user.is_exists(user_id):
                                await state.update_data(user_id=user_id)
                                await AdminWindow.add_admin_confirm(state, message=message)
                            else:
                                text = (
                                    f"<b>Пользователь с ID {user_id} не найден.</b>"
                                )
                                await AdminWindow.add_admin(state, message=message, text=text)
                    else:
                        text = (
                            "<b>ID пользователя должен быть числом.</b>"
                        )
                        await AdminWindow.add_admin(state, message=message, text=text)
            case _:
                await delete_message(message)
