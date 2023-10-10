from aiogram import Dispatcher

from app.config import Config


async def on_startup(dp: Dispatcher):
    config: Config = dp.bot.get("config")

    from .db.mysql.manage import Database
    db: Database = Database(config.database)
    await db.init()
    dp.bot["db"] = db

    from .db.scheduler.manage import Scheduler
    scheduler: Scheduler = Scheduler()
    scheduler.async_scheduler.start()
    dp.bot["scheduler"] = scheduler

    from .bot import filters
    filters.setup(dp)

    from .bot import middlewares
    middlewares.setup(dp)

    from .bot import handlers
    handlers.errors.register(dp)
    handlers.commands.register(dp)
    handlers.messages.register(dp)
    handlers.callbacks.register(dp)


async def on_shutdown(dp: Dispatcher):
    from .db.mysql.manage import Database
    db: Database = dp.bot.get("db")
    await db.close()

    from .db.scheduler.manage import Scheduler
    scheduler: Scheduler = dp.bot.get("scheduler")
    scheduler.async_scheduler.shutdown()

    await dp.storage.close()
    await dp.storage.wait_closed()

    session = await dp.bot.get_session()
    await session.close()
