from dataclasses import dataclass
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hcode

from app.bot import keyboards
from app.bot.misc.createtexts import create_info_token_text
from app.bot.misc.messages import delete_previous_message
from app.bot.states import PostMenuState
from app.db.scheduler.manage import Scheduler
from app.db.sqlite.manage import Database


@dataclass
class PostWindow:

    # noinspection PyUnusedLocal
    @staticmethod
    async def menu(state: FSMContext, call: CallbackQuery) -> None:
        scheduler: Scheduler = call.bot.get("scheduler")

        posts: list[tuple] = [
            (job.next_run_time.strftime("%d.%m.%Y %H:%M"), job.id)
            for job in scheduler.async_scheduler.get_jobs()
        ]

        markup = keyboards.post_menu(posts)
        text = "<b>Меню управления отложенными постами:</b>"

        await call.message.edit_text(text, reply_markup=markup)
        await PostMenuState.menu.set()

    @staticmethod
    async def info_post(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        scheduler: Scheduler = call.bot.get("scheduler")
        db: Database = message.bot.get("db") if message else call.bot.get("db")

        job = scheduler.async_scheduler.get_job(data["job_id"])
        token_id, channels_ids = job.args

        token = await db.token.get(token_id)
        time = job.next_run_time.strftime("%d.%m.%Y %H:%M")

        markup = keyboards.post_info()
        text = create_info_token_text(token)
        text += (
            f"\n\n<b>Время запуска рассылки:</b> {time}"
        )

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await PostMenuState.info_post.set()

    @staticmethod
    async def edit_time(state: FSMContext, message: Message = None, call: CallbackQuery = None,
                        text: str = None) -> None:
        data = await state.get_data()
        scheduler: Scheduler = message.bot.get("scheduler") if message else call.bot.get("scheduler")

        job = scheduler.async_scheduler.get_job(data["job_id"])
        next_time = job.next_run_time.strftime("%d.%m.%Y %H:%M")

        markup = keyboards.back()
        if not text: text = (  # noqa:E701
            f"<b>Дата и время рассылки:</b> <code>{next_time}</code>\n\n"
            "<b>Пришлите новую дату и время:</b>"
        )

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await PostMenuState.edit_time.set()

    @staticmethod
    async def edit_time_confirm(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")
        scheduler: Scheduler = message.bot.get("scheduler") if message else call.bot.get("scheduler")

        job = scheduler.async_scheduler.get_job(data["job_id"])
        token_id, channels_ids = job.args
        token = await db.token.get(token_id)

        current_next_time = job.next_run_time.strftime("%d.%m.%Y %H:%M")
        new_next_time = datetime.strptime(data["new_time"], "%d.%m.%Y %H:%M").strftime("%d.%m.%Y %H:%M")

        markup = keyboards.back_confirm()
        text = create_info_token_text(token)
        text += (
            f"\n\n<b>Подтвердите изменение времени с {current_next_time} "
            f"на {new_next_time}.</b>"
        )

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await PostMenuState.edit_time_confirm.set()

    @staticmethod
    async def edit_comment(state: FSMContext, message: Message = None, call: CallbackQuery = None,
                           text: str = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")
        scheduler: Scheduler = message.bot.get("scheduler") if message else call.bot.get("scheduler")

        job = scheduler.async_scheduler.get_job(data["job_id"])
        token_id, channels_ids = job.args
        token = await db.token.get(token_id)

        markup = keyboards.back()
        if not text:
            text = "" if not token.comment else (
                "<b>Старый комментарий:</b>\n"
                f"{hcode(token.comment)}\n\n"
            )
            text += "<b>Пришлите новый комментарий:</b>"

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await PostMenuState.edit_comment.set()

    @staticmethod
    async def edit_comment_confirm(state: FSMContext, message: Message = None, call: CallbackQuery = None) -> None:
        data = await state.get_data()
        db: Database = message.bot.get("db") if message else call.bot.get("db")
        scheduler: Scheduler = message.bot.get("scheduler") if message else call.bot.get("scheduler")

        job = scheduler.async_scheduler.get_job(data["job_id"])
        token_id, channels_ids = job.args
        token = await db.token.get(token_id)

        markup = keyboards.back_confirm()
        text = "" if not token.comment else (
            "<b>Старый комментарий:</b>\n"
            f"{hcode(token.comment)}\n\n"
        )
        text += (
            "<b>Новый комментарий:</b>\n\n"
            f"{hcode(data['new_comment'])}\n\n"
            f"<b>Подтвердите изменение комментария:</b>"
        )

        if message:
            await delete_previous_message(message.bot, state)
            msg = await message.answer(text, reply_markup=markup)
            await state.update_data(message_id=msg.message_id)
        else:
            await call.message.edit_text(text, reply_markup=markup)
        await PostMenuState.edit_comment_confirm.set()

    @staticmethod
    async def del_post_confirm(state: FSMContext, call: CallbackQuery) -> None:
        data = await state.get_data()
        db: Database = call.bot.get("db")
        scheduler: Scheduler = call.bot.get("scheduler")

        job = scheduler.async_scheduler.get_job(data["job_id"])
        next_time = job.next_run_time.strftime("%d.%m.%Y %H:%M")
        token_id, channels_ids = job.args
        token = await db.token.get(token_id)

        markup = keyboards.back_confirm()
        text = create_info_token_text(token)
        text += (
            f"\n\n<b>Рассылка отложена до {next_time}</b>\n\n"
            "<b>Подтвердите удаление отложенного поста:</b>"
        )

        await call.message.edit_text(text, reply_markup=markup)
        await PostMenuState.del_post_confirm.set()
