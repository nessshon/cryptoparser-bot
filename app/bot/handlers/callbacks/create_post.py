import asyncio
from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.bot import keyboards
from app.bot.handlers.windows.create_post import CreatePostWindow
from app.bot.handlers.windows.main import MainWindow
from app.bot.keyboards import CallbackData
from app.bot.misc.startposts import send_posts
from app.bot.misc.throttling import ThrottlingContext
from app.db.sqlite.manage import Database


@dataclass
class CreatePostCallback:

    @staticmethod
    async def send_message_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await MainWindow.menu(state, call=call)
        await call.answer()

    @staticmethod
    async def send_buttons_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await CreatePostWindow.send_message(state, call=call)
            case CallbackData.SKIP:
                await state.update_data(buttons=None)
                await CreatePostWindow.choose_channel(state, call=call)
        await call.answer()

    @staticmethod
    async def choose_channel_handler(call: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")

        selected: list = [] if "selected" not in data else data["selected"]
        channels_ids = [channel.id for channel in await db.channel.get_all()]

        match call.data:
            case CallbackData.BACK:
                async with state.proxy() as data:
                    data.pop("selected")
                await CreatePostWindow.send_buttons(state, call=call)
            case CallbackData.NEXT:
                if len(selected) > 0:
                    text, photo, buttons = data["text"], data["photo"], data["buttons"]
                    markup = keyboards.generate_buttons(buttons) if buttons else None
                    if photo:
                        await call.message.answer_photo(photo, caption=text, reply_markup=markup)
                    else:
                        await call.message.answer(text, reply_markup=markup)
                    await CreatePostWindow.send_confirm(state, message=call.message)
                else:
                    text = "Нужно выбрать минимум 1 канал!"
                    await call.answer(text, show_alert=True)
            case CallbackData.ALL:
                if len(selected) == len(channels_ids):
                    selected.clear()
                else:
                    selected = channels_ids
                await state.update_data(selected=selected)
                await CreatePostWindow.choose_channel(state, call=call)

            case channel_id if int(channel_id) in channels_ids:
                if int(channel_id) in selected:
                    selected.remove(int(channel_id))
                else:
                    selected.append(int(channel_id))
                await state.update_data(selected=selected)
                await CreatePostWindow.choose_channel(state, call=call)
        await call.answer()

    @staticmethod
    async def send_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()

        match call.data:
            case CallbackData.BACK:
                await CreatePostWindow.choose_channel(state, call=call)
            case CallbackData.CONFIRM:
                async with ThrottlingContext(state):
                    text, photo, = data["text"], data["photo"]
                    buttons, channels_ids = data["buttons"], data["selected"]
                    asyncio.create_task(send_posts(channels_ids, text, photo, buttons))
                    text = "Рассылка запущена!"
                    await call.answer(text, show_alert=True)
                    await MainWindow.menu(state, call=call)
                async with state.proxy() as data:
                    data.pop("text")
                    data.pop("photo")
                    data.pop("buttons")
                    data.pop("selected")
        await call.answer()
