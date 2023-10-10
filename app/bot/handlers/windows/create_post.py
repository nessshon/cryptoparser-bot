from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot import keyboards
from app.bot.misc.messages import delete_previous_message
from app.bot.states import CreatePostState
from app.db.mysql.manage import Database


@dataclass
class CreatePostWindow:

    @staticmethod
    async def send_message(state: FSMContext, message: Message = None, call: CallbackQuery = None,
                           text: str = None) -> None:
        markup = keyboards.back()
        if not text: text = "<b>Отправьте или перешлите сообщение:</b>"  # noqa:E701

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await CreatePostState.send_message.set()

    @staticmethod
    async def send_buttons(state: FSMContext, message: Message = None, call: CallbackQuery = None,
                           text: str = None) -> None:
        markup = keyboards.back_skip()
        if not text: text = "<b>Отправьте URL-кнопки к посту в формате:</b>\n\n"  # noqa:E701
        text += (
            "<code>Текст кнопки | ссылка</code>\n"
            "Пример:\n"
            "<code>Текст | https://example.com</code>\n\n"
            "Чтобы добавить несколько кнопок в один ряд, пришлите ссылки через запятую.\n"
            "Формат:\n"
            "<code>Первый текст | https://example.com, Второй текст | https://example.com</code>\n\n"
            "Чтобы добавить несколько кнопок в колонку, пришлите новые кнопки с новой строки.\n"
            "Формат:\n"
            "<code>Первый текст | https://example.com\nВторой текст | https://example.com</code>"
        )
        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await CreatePostState.send_buttons.set()

    @staticmethod
    async def choose_channel(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        channels = await db.channel.get_all()
        selected: list = [] if "selected" not in data else data["selected"]

        markup = keyboards.choose_channels(channels, selected)
        text = "<b>Выберите каналы в которых хотите опубликовать пост:</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await CreatePostState.choose_channel.set()

    @staticmethod
    async def send_confirm(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        markup = keyboards.back_confirm()
        text = "Перепроверьте сообщение выше.\n\n<b>Подтвердите рассылку поста:</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await CreatePostState.send_confirm.set()
