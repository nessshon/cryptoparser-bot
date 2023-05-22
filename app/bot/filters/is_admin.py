from aiogram.types import Message, CallbackQuery, User
from aiogram.dispatcher.filters import BoundFilter

from app.config import Config
from app.db.sqlite.manage import Database


class IsAdmin(BoundFilter):

    async def check(self, update: Message | CallbackQuery) -> bool:
        config: Config = update.bot.get("config")
        db: Database = update.bot.get("db")
        user: User = User.get_current()

        if user.id in [config.ADMIN_ID, config.DEV_ID]:
            return True

        db_user = await db.user.get(user.id)
        return db_user.is_admin if db_user else False
