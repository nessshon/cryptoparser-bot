import asyncio
import logging
import random
import datetime
import signal

import pytz

from app.config import load_config, Config
from app.db.mysql.manage import Database
from app.parser.main import parse


async def on_startup(db: Database, config: Config):
    """
    Function to run on application startup.
    Initializes the database and starts the parsing process.
    """
    logging.info("Starting...")

    await db.init()
    logging.info("Database initialized!")

    while True:
        now = datetime.datetime.now(tz=pytz.timezone("Europe/Moscow")).time()
        if now >= datetime.time(23, 0) or now < datetime.time(8, 0):
            logging.info("Skipping parsing...")
            await asyncio.sleep(600)
            continue
        logging.info("Parsing...")
        asyncio.create_task(parse(db, config))
        logging.info("Parsing added to the task...")
        await asyncio.sleep(random.randint(2400, 3600))


async def on_shutdown(db: Database):
    """
    Function to run on application shutdown.
    Closes the database connection.
    """
    await db.close()
    logging.warning("Database session closed!")


def init() -> None:
    """
    Main function to run the application.
    Sets up logging, initializes the database and bot, and starts the event loop.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # noqa
    )
    config = load_config()
    db = Database(config.database)

    # Create an asyncio event loop
    loop = asyncio.get_event_loop()
    # Add signal handler for graceful shutdown
    loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(on_shutdown(db)))

    try:
        # Run the on_startup function
        loop.run_until_complete(on_startup(db, config))
    except (KeyboardInterrupt, SystemExit):
        pass

    # Run the on_shutdown function
    loop.run_until_complete(on_shutdown(db))
    # Close the event loop
    loop.close()


if __name__ == "__main__":
    init()
