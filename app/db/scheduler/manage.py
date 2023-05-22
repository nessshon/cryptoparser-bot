from datetime import datetime
from pathlib import Path

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.bot.misc.startposts import start_posts
from app.config import TIME_ZONE

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = f"{BASE_DIR}/scheduler.sqlite3"


class Scheduler:

    def __init__(self):
        stores = {
            "default": SQLAlchemyJobStore(
                url=f"sqlite:///{DB_PATH}"
            )
        }
        self.async_scheduler = AsyncIOScheduler(
            jobstores=stores,
            timezone=TIME_ZONE,
        )

    def add_postpone_post(self, time: str, token_id: int, channels_ids: list) -> None:
        time = datetime.strptime(time, "%d.%m.%Y %H:%M")

        self.async_scheduler.add_job(
            func=start_posts,
            args=(token_id, channels_ids),
            id=f"post_{token_id}",
            replace_existing=True,
            misfire_grace_time=10,
            run_date=time
        )
