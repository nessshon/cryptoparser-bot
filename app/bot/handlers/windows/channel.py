from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hlink

from app.bot import keyboards
from app.bot.misc.messages import delete_previous_message
from app.bot.states import ChannelMenuState
from app.db.mysql.manage import Database
from app.translator import SUPPORT_LANGUAGES


@dataclass
class ChannelWindow:

    @staticmethod
    async def menu(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        db: Database = message.bot.get("db") if message else call.bot.get("db")
        channels = await db.channel.get_all()

        markup = keyboards.channel_menu(channels)
        text = "<b>Меню управления каналами:</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.menu.set()

    @staticmethod
    async def add_channel(state: FSMContext, message: Message = None, call: CallbackQuery = None,
                          text: str = None) -> None:
        markup = keyboards.back()
        if not text: text = (  # noqa:E701
            "<b>Для добавления канала, пришлите ID канала "
            "или перешлите любое сообщение от него:</b>"
        )

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.add_channel.set()

    @staticmethod
    async def add_channel_choose_lang(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        url = f"tg://openmessage?chat_id={str(data['channel_id'])[3:]}"
        channel_link = hlink(data["channel_title"], url)

        markup = keyboards.support_languages()
        text = f"<b>Выберите язык для канала {channel_link}:</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.add_channel_choose_lang.set()

    @staticmethod
    async def add_channel_confirm(state: FSMContext, call: CallbackQuery) -> None:
        data = await state.get_data()
        url = f"tg://openmessage?chat_id={str(data['channel_id'])[3:]}"
        channel_link = hlink(data["channel_title"], url)

        markup = keyboards.back_confirm()
        text = (
            f"<b>Вы уверены, что хотите добавить канал {channel_link} "
            f"и присвоить ему {SUPPORT_LANGUAGES.get(data['channel_lang'])} язык?</b>"
        )

        await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.add_channel_confirm.set()

    @staticmethod
    async def info_channel(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        channel = await db.channel.get(id_=data["channel_id"])
        url = f"tg://openmessage?chat_id={str(data['channel_id'])[3:]}"
        channel_link = hlink(channel.title, url)

        markup = keyboards.channel_info()
        text = (
            f"{channel_link}\n\n"
            f"<b>Название канала:</b> {channel.title}\n"
            f"<b>Язык канала:</b> {SUPPORT_LANGUAGES.get(channel.language_code).lower()}\n"
            f"<b>Дата добавления:</b> {channel.created_at.strftime('%Y-%m-%d %H:%M')}"
        )

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.info_channel.set()

    @staticmethod
    async def del_channel_confirm(state: FSMContext, call: CallbackQuery) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")

        channel = await db.channel.get(id_=data["channel_id"])
        url = f"tg://openmessage?chat_id={str(data['channel_id'])[3:]}"
        channel_link = hlink(channel.title, url)

        markup = keyboards.back_confirm()
        text = f"<b>Вы уверены, что хотите удалить канал {channel_link}?</b>"

        await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.del_channel_confirm.set()

    @staticmethod
    async def edit_title(state: FSMContext, message: Message = None, call: CallbackQuery = None,
                         text: str = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        channel = await db.channel.get(id_=data["channel_id"])
        url = f"tg://openmessage?chat_id={str(data['channel_id'])[3:]}"
        channel_link = hlink(channel.title, url)

        markup = keyboards.back()
        if not text: text = f"<b>Пришлите новое название канала {channel_link}?</b>"  # noqa:E701

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.edit_title.set()

    @staticmethod
    async def edit_title_confirm(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        channel = await db.channel.get(id_=data["channel_id"])
        url = f"tg://openmessage?chat_id={str(data['channel_id'])[3:]}"
        channel_link = hlink(channel.title, url)

        markup = keyboards.back_confirm()
        text = (
            f"<b>Вы уверены, что хотите изменить название канала "
            f" {channel_link} на {data['new_channel_title']}?</b>"
        )

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.edit_title_confirm.set()

    @staticmethod
    async def edit_lang(state: FSMContext, call: CallbackQuery) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")

        channel = await db.channel.get(id_=data["channel_id"])
        url = f"tg://openmessage?chat_id={str(data['channel_id'])[3:]}"
        channel_link = hlink(channel.title, url)

        markup = keyboards.support_languages()
        text = f"<b>Выберите новый язык для канала {channel_link}:</b>"

        await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.edit_lang.set()

    @staticmethod
    async def edit_lang_confirm(state: FSMContext, call: CallbackQuery):
        data = await state.get_data()
        db: Database = call.bot.get("db")

        channel = await db.channel.get(id_=data["channel_id"])
        url = f"tg://openmessage?chat_id={str(data['channel_id'])[3:]}"
        channel_link = hlink(channel.title, url)

        markup = keyboards.back_confirm()
        text = (
            f"<b>Вы уверены, что хотите изменить язык канала {channel_link} "
            f"с {SUPPORT_LANGUAGES.get(channel.language_code)} "
            f"на {SUPPORT_LANGUAGES.get(data['new_channel_lang'])}?</b>"
        )

        await call.message.edit_text(text, reply_markup=markup)
        await ChannelMenuState.edit_lang_confirm.set()
