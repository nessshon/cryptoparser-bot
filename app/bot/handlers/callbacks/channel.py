from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.bot.handlers.windows.channel import ChannelWindow
from app.bot.handlers.windows.main import MainWindow
from app.bot.keyboards import CallbackData
from app.bot.misc.throttling import rate_limit, ThrottlingContext
from app.db.sqlite.manage import Database
from app.translator import SUPPORT_LANGUAGES


@dataclass
class ChannelCallback:

    @staticmethod
    async def menu_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await MainWindow.menu(state, call=call)
            case CallbackData.ADD:
                await ChannelWindow.add_channel(state, call=call)
            case channel_id if channel_id.startswith("-100"):
                await state.update_data(channel_id=int(channel_id))
                await ChannelWindow.info_channel(state, call=call)
        await call.answer()

    @staticmethod
    async def add_channel_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await ChannelWindow.menu(state, call=call)
        await call.answer()

    @staticmethod
    async def add_channel_choose_lang_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await ChannelWindow.add_channel(state, call=call)
            case lang if lang in SUPPORT_LANGUAGES.keys():
                await state.update_data(channel_lang=lang)
                await ChannelWindow.add_channel_confirm(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def add_channel_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await ChannelWindow.add_channel_choose_lang(state, call=call)
            case CallbackData.CONFIRM:
                data = await state.get_data()
                db: Database = call.bot.get("db")

                async with ThrottlingContext(state):
                    await db.channel.add(
                        id=data["channel_id"],
                        title=data["channel_title"],
                        language_code=data["channel_lang"],
                    )
                    text = f"Канал успешно добавлен!"
                    await call.answer(text, show_alert=True)
                    await ChannelWindow.menu(state, call=call)
        await call.answer()

    @staticmethod
    async def info_channel_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await ChannelWindow.menu(state, call=call)
            case CallbackData.DELETE:
                await ChannelWindow.del_channel_confirm(state, call=call)
            case CallbackData.EDIT_TITLE:
                await ChannelWindow.edit_title(state, call=call)
            case CallbackData.EDIT_LANGUAGE:
                await ChannelWindow.edit_lang(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def del_channel_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await ChannelWindow.info_channel(state, call=call)
            case CallbackData.CONFIRM:
                data = await state.get_data()
                db: Database = call.bot.get("db")

                async with ThrottlingContext(state):
                    channel = await db.channel.get(id_=data["channel_id"])
                    await db.channel.delete(id_=data["channel_id"])
                    text = f"Канал {channel.title} успешно удален!"
                    await call.answer(text, show_alert=True)
                    await ChannelWindow.menu(state, call=call)
        await call.answer()

    @staticmethod
    async def edit_title_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await ChannelWindow.info_channel(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def edit_title_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await ChannelWindow.edit_title(state, call=call)
            case CallbackData.CONFIRM:
                data = await state.get_data()
                db: Database = call.bot.get("db")

                async with ThrottlingContext(state):
                    channel = await db.channel.get(id_=data["channel_id"])
                    await db.channel.update(
                        id_=data["channel_id"],
                        title=data["new_channel_title"],
                    )
                    text = (
                        f"Название канала {channel.title} успешно изменено "
                        f"на {data['new_channel_title']}!"
                    )
                    await call.answer(text, show_alert=True)
                    await ChannelWindow.menu(state, call=call)
        await call.answer()

    @staticmethod
    async def edit_lang_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await ChannelWindow.info_channel(state, call=call)
            case lang if lang in SUPPORT_LANGUAGES.keys():
                await state.update_data(new_channel_lang=lang)
                await ChannelWindow.edit_lang_confirm(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def edit_lang_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await ChannelWindow.edit_lang(state, call=call)
            case CallbackData.CONFIRM:
                data = await state.get_data()
                db: Database = call.bot.get("db")

                async with ThrottlingContext(state):
                    channel = await db.channel.get(id_=data["channel_id"])
                    await db.channel.update(
                        id_=data["channel_id"],
                        language_code=data["new_channel_lang"],
                    )
                    text = (
                        f"Язык канала {channel.title} успешно изменен "
                        f"на {SUPPORT_LANGUAGES.get(data['new_channel_lang'])}!"
                    )
                    await call.answer(text, show_alert=True)
                    await ChannelWindow.menu(state, call=call)
        await call.answer()
