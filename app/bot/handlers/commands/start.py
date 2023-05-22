from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.bot.handlers.windows.main import MainWindow
from app.bot.misc.throttling import rate_limit
from app.config import Config
from app.db.sqlite.manage import Database


@rate_limit(1, "sleep")
async def start_command(message: Message, state: FSMContext) -> None:
    db: Database = message.bot.get("db")
    config: Config = message.bot.get("config")

    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if user_id in [config.ADMIN_ID, config.DEV_ID]:
        user_is_admin = True
    else:
        db_user = await db.user.get(user_id)
        if db_user is None: db_user = await db.user.add(id=user_id, first_name=first_name)  # noqa:E701
        user_is_admin = db_user.is_admin

    if user_is_admin: await MainWindow.menu(state, message)  # noqa:E701
