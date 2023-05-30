from contextlib import suppress
from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.bot.handlers.windows.admin import AdminWindow
from app.bot.handlers.windows.channel import ChannelWindow
from app.bot.handlers.windows.create_post import CreatePostWindow
from app.bot.handlers.windows.post import PostWindow
from app.bot.handlers.windows.token import TokenWindow
from app.bot.keyboards import CallbackData
from app.bot.misc.messages import delete_previous_message


@dataclass
class MainCallback:

    @staticmethod
    async def handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case data if data.startswith("token:h"):
                with suppress(Exception):
                    await call.message.delete()
            case data if data.startswith("token:o"):
                _, token_id = data.split(":o")
                await delete_previous_message(call.bot, state)
                await state.update_data(
                    token_id=token_id,
                    message_id=call.message.message_id,
                )
                await TokenWindow.info_token(state, call=call)
            case data if data.startswith("token:d"):
                _, token_id = data.split(":d")
                await delete_previous_message(call.bot, state)
                await state.update_data(
                    token_id=token_id,
                    message_id=call.message.message_id,
                )
                await TokenWindow.del_token_confirm(state, call=call)

        await call.answer()

    @staticmethod
    async def menu_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.CREATE_POST:
                await CreatePostWindow.send_message(state, call=call)
            case CallbackData.ADMINS:
                await AdminWindow.menu(state, call=call)
            case CallbackData.CHANNELS:
                await ChannelWindow.menu(state, call=call)
            case CallbackData.TOKENS:
                await TokenWindow.menu(state, call=call)
            case CallbackData.PENDING:
                await PostWindow.menu(state, call=call)
        await call.answer()
