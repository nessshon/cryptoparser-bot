from dataclasses import dataclass
from datetime import datetime

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from app.bot import keyboards
from app.bot.misc.messages import delete_previous_message
from app.bot.misc.createtexts import create_base_info_token_text, create_info_token_text
from app.bot.states import TokenMenuState
from app.config import TIME_ZONE
from app.db.sqlite.manage import Database


@dataclass
class TokenWindow:

    # noinspection PyUnusedLocal
    @staticmethod
    async def menu(state: FSMContext, call: CallbackQuery) -> None:
        db: Database = call.bot.get("db")

        tokens = await db.token.get_not_viewed_all()

        markup = keyboards.token_menu(tokens)
        text = "<b>Меню управления токенами:</b>"

        await call.message.edit_text(text, reply_markup=markup)
        await TokenMenuState.menu.set()

    @staticmethod
    async def info_token(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        token = await db.token.get(id_=data["token_id"])

        markup = keyboards.token_info()
        text = create_base_info_token_text(token)

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await TokenMenuState.info_token.set()

    @staticmethod
    async def create_post(state: FSMContext, message: Message = None, call: CallbackQuery = None,
                          text: str = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        token = await db.token.get(id_=data["token_id"])

        markup = keyboards.back_skip()
        if not text:
            text = create_base_info_token_text(token)
            text += "\n\n<b>Пришлите комментарий к токену:</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await TokenMenuState.create_post.set()

    @staticmethod
    async def choose_channel(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        token = await db.token.get(id_=data["token_id"])
        channels = await db.channel.get_all()
        selected: list = [] if "selected" not in data else data["selected"]

        markup = keyboards.choose_channels(channels, selected)
        text = create_info_token_text(token)
        text += "\n\n<b>Выберите каналы в которых хотите опубликовать пост:</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await TokenMenuState.choose_channel.set()

    @staticmethod
    async def choose_time(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        token = await db.token.get(id_=data["token_id"])

        markup = keyboards.choose_time()
        text = create_info_token_text(token)
        text += "\n\n<b>Выберите, отложить или запустить рассылку постов:</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await TokenMenuState.choose_time.set()

    @staticmethod
    async def create_post_confirm(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        token = await db.token.get(id_=data["token_id"])

        markup = keyboards.back_confirm()
        text = create_info_token_text(token)
        text += "\n\n<b>Подтвердите запуск рассылки поста:</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await TokenMenuState.create_post_confirm.set()

    @staticmethod
    async def send_time(state: FSMContext, message: Message = None, call: CallbackQuery = None,
                        text: str = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        token = await db.token.get(id_=data["token_id"])
        markup = keyboards.back()
        if text:
            text = create_info_token_text(token) + f"\n\n{text}"
        else:
            text = create_info_token_text(token)
            current_date = datetime.now(tz=pytz.timezone(TIME_ZONE)).strftime("%d.%m.%Y %H:%M")
            text += (
                "\n\n<b>Отправьте время в формате</b> "
                "<code>ДД.ММ.ГГГГ ЧЧ:ММ</code>:\n\n"
                f"Пример: <code>{current_date}</code>"
            )

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await TokenMenuState.send_time.set()

    @staticmethod
    async def create_postpone_confirm(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        token = await db.token.get(id_=data["token_id"])

        markup = keyboards.back_confirm()
        text = create_info_token_text(token)
        text += f"\n\n<b>Подтвердите отложение поста на {data['time']}</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await TokenMenuState.create_postpone_confirm.set()

    @staticmethod
    async def del_token_confirm(state: FSMContext, call: CallbackQuery) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")

        token = await db.token.get(id_=data["token_id"])
        text = create_base_info_token_text(token)
        text += "\n\n<b>Подтвердите удаление токена:</b>"
        markup = keyboards.back_confirm()

        await call.message.edit_text(text, reply_markup=markup)
        await TokenMenuState.del_token_confirm.set()
