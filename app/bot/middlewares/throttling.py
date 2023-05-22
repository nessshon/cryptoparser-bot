from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self,
                 key: str = 'default',
                 call_limit: float = 0.5,
                 message_limit: float = 0.5
                 ):
        self.default_key = key
        self.call_limit = call_limit
        self.message_limit = message_limit
        super(ThrottlingMiddleware, self).__init__()

    # noinspection PyUnusedLocal
    async def on_process_message(self, message: Message, data: dict):
        dispatcher = Dispatcher.get_current()
        handler = current_handler.get()

        if handler:
            throttling_key = getattr(handler, "throttling_key", None)
            key = throttling_key if throttling_key else self.default_key
            limit = getattr(handler, "throttling_rate_limit", self.message_limit)

            if key == "sleep":
                state: FSMContext = data.get("state", None)
                user_data = await state.get_data()
                if "sleep" in user_data and user_data["sleep"]:
                    raise CancelHandler()

        else:
            limit = self.message_limit
            key = self.default_key

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled:
            raise CancelHandler()

    # noinspection PyUnusedLocal
    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        dispatcher = Dispatcher.get_current()
        handler = current_handler.get()

        if handler:
            throttling_key = getattr(handler, "throttling_key", None)
            key = throttling_key if throttling_key else self.default_key
            limit = getattr(handler, "throttling_rate_limit", self.call_limit)

            if key == "sleep":
                state: FSMContext = data.get("state", None)
                user_data = await state.get_data()
                if "sleep" in user_data and user_data["sleep"]:
                    raise CancelHandler()

        else:
            limit = self.call_limit
            key = self.default_key

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled:
            raise CancelHandler()
