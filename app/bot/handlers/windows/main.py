from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hide_link

from app.bot import keyboards
from app.bot.misc.messages import delete_previous_message
from app.bot.states import MainState
from app.config import Config, DEFAULT_BANNER_URL


@dataclass
class MainWindow:

    @staticmethod
    async def menu(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        user_id = message.from_user.id if message else call.from_user.id
        config: Config = message.bot.get("config") if message else call.bot.get("config")

        markup = keyboards.main_menu(config, user_id)
        text = "<b>Выберите действие:</b>"
        text += hide_link(DEFAULT_BANNER_URL)

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await MainState.menu.set()
