from aiogram.dispatcher import FSMContext


class ThrottlingContext:
    def __init__(self, state: FSMContext):
        self.state = state

    async def __aenter__(self):
        await self.state.update_data(sleep=True)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.state.update_data(sleep=False)


def rate_limit(limit: float, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)

        return func

    return decorator
