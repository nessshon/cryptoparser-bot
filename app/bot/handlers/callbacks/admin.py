from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.bot.handlers.windows.admin import AdminWindow
from app.bot.handlers.windows.main import MainWindow
from app.bot.keyboards import CallbackData
from app.bot.misc.throttling import ThrottlingContext, rate_limit
from app.db.mysql.manage import Database


@dataclass
class AdminCallback:

    @staticmethod
    async def menu_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await MainWindow.menu(state, call=call)
            case CallbackData.ADD:
                await AdminWindow.add_admin(state, call=call)
            case user_id if user_id.isdigit():
                await state.update_data(user_id=int(user_id))
                await AdminWindow.info_admin(state, call=call)
        await call.answer()

    @staticmethod
    async def add_admin_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await AdminWindow.menu(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def add_admin_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await AdminWindow.add_admin(state, call=call)
            case CallbackData.CONFIRM:
                data = await state.get_data()
                db: Database = call.bot.get("db")

                async with ThrottlingContext(state):
                    await db.user.update(id_=data["user_id"], is_admin=True)
                    text = "Администратор успешно добавлен!"
                    await call.answer(text, show_alert=True)
                    await AdminWindow.menu(state, call=call)
        await call.answer()

    @staticmethod
    async def info_admin_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await AdminWindow.menu(state, call=call)
            case CallbackData.DELETE:
                await AdminWindow.del_admin_confirm(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def del_admin_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await AdminWindow.info_admin(state, call=call)
            case CallbackData.CONFIRM:
                data = await state.get_data()
                db: Database = call.bot.get("db")

                async with ThrottlingContext(state):
                    await db.user.update(id_=data["user_id"], is_admin=False)
                    text = "Администратор успешно удален!"
                    await call.answer(text, show_alert=True)
                    await AdminWindow.menu(state, call=call)
        await call.answer()
