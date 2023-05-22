from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hlink

from app.bot import keyboards
from app.bot.misc.messages import delete_previous_message
from app.bot.states import AdminMenuState
from app.db.sqlite.manage import Database


@dataclass
class AdminWindow:

    @staticmethod
    async def menu(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        db: Database = call.bot.get("db")

        admins = await db.user.get_all_admins()
        markup = keyboards.admin_menu(admins if admins else [])
        text = "<b>Меню управления администраторами:</b>\n"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await AdminMenuState.menu.set()

    @staticmethod
    async def add_admin(state: FSMContext, message: Message = None, call: CallbackQuery = None,
                        text: str = None) -> None:
        markup = keyboards.back()
        if not text: text = (  # noqa:E701
            "<b>Для добавления администратора, пришлите ID пользователя "
            "или перешлите любое сообщение от него:</b>"
        )

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await AdminMenuState.add_admin.set()

    @staticmethod
    async def add_admin_confirm(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        user = await db.user.get(id_=data["user_id"])
        user_link = hlink(title=user.first_name, url=f"tg://user?id={user.id}")

        markup = keyboards.back_confirm()
        text = f"<b>Подтвердить добавление администратора {user_link}?</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await AdminMenuState.add_admin_confirm.set()

    @staticmethod
    async def info_admin(state: FSMContext, call: CallbackQuery) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")

        user = await db.user.get(id_=data["user_id"])
        user_link = hlink(title=user.first_name, url=f"tg://user?id={user.id}")

        markup = keyboards.admin_info()
        text = (
            f"{user_link}\n\n"
            f"<b>ID:</b> {user.id}\n"
            f"<b>Имя:</b> {user.first_name}\n"
            f"<b>Дата регистрации:</b> {user.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        )

        await call.message.edit_text(text, reply_markup=markup)
        await AdminMenuState.info_admin.set()

    @staticmethod
    async def del_admin_confirm(state: FSMContext, call: CallbackQuery) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")

        user = await db.user.get(id_=data["user_id"])
        user_link = hlink(title=user.first_name, url=f"tg://user?id={user.id}")

        markup = keyboards.back_confirm()
        text = f"<b>Подтвердить удаление администратора {user_link}?</b>"

        await call.message.edit_text(text, reply_markup=markup)
        await AdminMenuState.del_admin_confirm.set()
