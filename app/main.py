from aiogram import Dispatcher


async def on_startup(dp: Dispatcher):
    from .db.sqlite.manage import Database
    db: Database = Database()
    await db.run_sync()
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
    from .db.sqlite.manage import Database
    db: Database = dp.bot.get("db")
    await db.engine.dispose()

    from .db.scheduler.manage import Scheduler
    scheduler: Scheduler = dp.bot.get("scheduler")
    scheduler.async_scheduler.shutdown()

    await dp.storage.close()
    await dp.storage.wait_closed()

    session = await dp.bot.get_session()
    await session.close()
