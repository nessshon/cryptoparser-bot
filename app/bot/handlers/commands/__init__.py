from aiogram import Dispatcher

from app.bot.filters import IsPrivate
from app.bot.handlers.commands.start import start_command


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(
        start_command, IsPrivate(),
        commands="start", state="*"
    )
