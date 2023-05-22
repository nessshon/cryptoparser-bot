import logging

from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.exceptions import Unauthorized

from app.config import load_config


def init():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
    )

    config = load_config()

    bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
    storage = RedisStorage2(host=config.REDIS_HOST)
    dp = Dispatcher(bot=bot, storage=storage)
    bot["config"] = config

    try:
        from . import main
        executor.start_polling(
            dispatcher=dp,
            skip_updates=False,
            reset_webhook=True,
            on_startup=main.on_startup,
            on_shutdown=main.on_shutdown,
        )

    except Unauthorized:
        logging.error("Invalid bot token!")

    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    init()
