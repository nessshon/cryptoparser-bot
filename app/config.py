from dataclasses import dataclass

from environs import Env

TIME_ZONE = "Europe/Moscow"
DEFAULT_BANNER_URL = "https://telegra.ph//file/54152190e759d280bddf1.jpg"


@dataclass
class Config:
    REDIS_HOST: str
    BOT_TOKEN: str
    ADMIN_ID: int
    DEV_ID: int


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        REDIS_HOST=env.str("REDIS_HOST"),
        BOT_TOKEN=env.str("BOT_TOKEN"),
        ADMIN_ID=env.int("ADMIN_ID"),
        DEV_ID=env.int("DEV_ID"),
    )
