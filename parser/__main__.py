import asyncio
import logging
import random

from aiogram import Bot

from app.config import load_config
from app.db.sqlite.manage import Database
from parser.main import parse


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
    )
    logging.info("Starting...")
    config = load_config()

    db: Database = Database()
    await db.run_sync()
    logging.info("Database initialized!")

    bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
    logging.info("Bot initialized!")

    while True:
        logging.info("Parsing...")
        await parse(db, bot, config)
        logging.info("Parsing finished!")
        await asyncio.sleep(random.randint(3400, 3800))


if __name__ == '__main__':
    asyncio.run(main())
