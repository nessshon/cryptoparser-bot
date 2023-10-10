import asyncio
import logging
import random
import datetime

import pytz

from app.config import load_config
from app.db.mysql.manage import Database
from app.parser.main import parse


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
    )
    logging.info("Starting...")
    config = load_config()

    db: Database = Database(config.database)
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


if __name__ == '__main__':
    asyncio.run(main())
