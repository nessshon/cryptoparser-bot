from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.bot.handlers.windows.main import MainWindow
from app.bot.handlers.windows.post import PostWindow
from app.bot.keyboards import CallbackData
from app.bot.misc.throttling import rate_limit, ThrottlingContext
from app.db.scheduler.manage import Scheduler
from app.db.mysql.manage import Database


@dataclass
class PostCallback:

    @staticmethod
    async def menu_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await MainWindow.menu(state, call=call)
            case job_id if job_id.startswith("post_"):
                async with state.proxy() as data:
                    data.pop("new_comment")
                    data.pop("new_time")
                await state.update_data(job_id=job_id)
                await PostWindow.info_post(state, call=call)
        await call.answer()

    @staticmethod
    async def info_post_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await PostWindow.menu(state, call=call)
            case CallbackData.EDIT_TIME:
                await PostWindow.edit_time(state, call=call)
            case CallbackData.EDIT_COMMENT:
                await PostWindow.edit_comment(state, call=call)
            case CallbackData.DELETE:
                await PostWindow.del_post_confirm(state, call=call)
        await call.answer()

    @staticmethod
    async def edit_time_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await PostWindow.info_post(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def edit_time_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        scheduler: Scheduler = call.bot.get("scheduler")

        match call.data:
            case CallbackData.BACK:
                await PostWindow.edit_time(state, call=call)
            case CallbackData.CONFIRM:
                async with ThrottlingContext(state):
                    job = scheduler.async_scheduler.get_job(data["job_id"])
                    token_id, channels_ids = job.args
                    scheduler.async_scheduler.remove_job(data["job_id"])
                    scheduler.add_postpone_post(data["new_time"], token_id, channels_ids)
                    text = "Время запуска рассылки успешно изменено!"
                    await call.answer(text, show_alert=True)
                    await PostWindow.info_post(state, call=call)
        await call.answer()

    @staticmethod
    async def edit_comment_handler(call: CallbackQuery, state: FSMContext) -> None:
        match call.data:
            case CallbackData.BACK:
                await PostWindow.info_post(state, call=call)
        await call.answer()

    @staticmethod
    async def edit_comment_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")
        scheduler: Scheduler = call.bot.get("scheduler")

        match call.data:
            case CallbackData.BACK:
                await PostWindow.edit_comment(state, call=call)
            case CallbackData.CONFIRM:
                async with ThrottlingContext(state):
                    job = scheduler.async_scheduler.get_job(data["job_id"])
                    token_id, channels_ids = job.args
                    await db.token.update(id_=token_id, comment=data["new_comment"])
                    text = "Комментарий успешно изменен!"
                    await call.answer(text, show_alert=True)
                    await PostWindow.info_post(state, call=call)
        await call.answer()

    @staticmethod
    @rate_limit(1, "sleep")
    async def del_post_confirm_handler(call: CallbackQuery, state: FSMContext) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")
        scheduler: Scheduler = call.bot.get("scheduler")

        match call.data:
            case CallbackData.BACK:
                await PostWindow.info_post(state, call=call)
            case CallbackData.CONFIRM:
                async with ThrottlingContext(state):
                    job = scheduler.async_scheduler.get_job(data["job_id"])
                    token_id, channels_ids = job.args
                    scheduler.async_scheduler.remove_job(data["job_id"])
                    await db.token.delete(token_id)
                    text = "Отложенный пост удален"
                    await call.answer(text, show_alert=True)
                    await PostWindow.menu(state, call=call)
        await call.answer()
