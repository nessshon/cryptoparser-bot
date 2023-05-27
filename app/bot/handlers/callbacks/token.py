import asyncio
from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.bot.handlers.windows.main import MainWindow
from app.bot.handlers.windows.token import TokenWindow
from app.bot.keyboards import CallbackData
from app.bot.misc.startposts import start_posts
from app.bot.misc.throttling import rate_limit, ThrottlingContext
from app.db.scheduler.manage import Scheduler
from app.db.sqlite.manage import Database


@dataclass
class TokenCallback:

    @staticmethod
    async def menu_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await MainWindow.menu(state, call=call)
            case token_id:
                async with state.proxy() as data:
                    data.pop("selected")
                    data.pop("comment")
                    data.pop("time")
                await state.update_data(token_id=token_id)
                await TokenWindow.info_token(state, call=call)
        await call.answer()

    @staticmethod
    async def info_token_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await TokenWindow.menu(state, call=call)
            case CallbackData.DELETE:
                await TokenWindow.del_token_confirm(state, call=call)
            case CallbackData.MAKE_POST:
                await TokenWindow.create_post(state, call=call)
        await call.answer()

    @staticmethod
    async def create_post_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await TokenWindow.info_token(state, call=call)
            case CallbackData.SKIP:
                await TokenWindow.choose_channel(state, call=call)
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
                await TokenWindow.create_post(state, call=call)
            case CallbackData.NEXT:
                if len(selected) > 0:
                    await TokenWindow.choose_time(state, call=call)
                else:
                    text = "Нужно выбрать минимум 1 канал!"
                    await call.answer(text, show_alert=True)
            case CallbackData.ALL:
                if len(selected) == len(channels_ids):
                    selected.clear()
                else:
                    selected = channels_ids
                await state.update_data(selected=selected)
                await TokenWindow.choose_channel(state, call=call)

            case channel_id if int(channel_id) in channels_ids:
                if int(channel_id) in selected:
                    selected.remove(int(channel_id))
                else:
                    selected.append(int(channel_id))
                await state.update_data(selected=selected)
                await TokenWindow.choose_channel(state, call=call)
        await call.answer()

    @staticmethod
    async def choose_time_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await TokenWindow.choose_channel(state, call=call)
            case CallbackData.START:
                await TokenWindow.create_post_confirm(state, call=call)
            case CallbackData.POSTPONE:
                await TokenWindow.send_time(state, call=call)
        await call.answer()

    @staticmethod
    async def send_time_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await TokenWindow.choose_time(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def create_postpone_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")
        scheduler: Scheduler = call.bot.get("scheduler")

        match call.data:
            case CallbackData.BACK:
                await TokenWindow.send_time(state, call=call)
            case CallbackData.CONFIRM:
                async with ThrottlingContext(state):
                    time, token_id, selected = data["time"], data["token_id"], data["selected"]
                    await db.token.update(token_id, is_viewed=True)
                    scheduler.add_postpone_post(time, token_id, selected)
                    text = f"Рассылка поста отложена на {time}"
                    await call.answer(text, show_alert=True)
                    await TokenWindow.menu(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def create_post_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")

        match call.data:
            case CallbackData.BACK:
                await TokenWindow.choose_time(state, call=call)
            case CallbackData.CONFIRM:
                async with ThrottlingContext(state):
                    token_id, selected = data["token_id"], data["selected"]
                    await db.token.update(id_=token_id, is_viewed=True)
                    asyncio.create_task(start_posts(token_id, selected))
                    text = "Рассылка запущена!"
                    await call.answer(text, show_alert=True)
                    await TokenWindow.menu(state, call=call)
                async with state.proxy() as data:
                    data.pop("selected")
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def del_token_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await TokenWindow.info_token(state, call=call)
            case CallbackData.CONFIRM:
                data = await state.get_data()
                db: Database = call.bot.get("db")

                async with ThrottlingContext(state):
                    await db.token.delete(data["token_id"])
                    text = "Токен удален!"
                    await call.answer(text, show_alert=True)
                await TokenWindow.menu(state, call=call)
        await call.answer()
