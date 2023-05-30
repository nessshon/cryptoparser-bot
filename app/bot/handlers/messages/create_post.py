from dataclasses import dataclass

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.bot import keyboards
from app.bot.handlers.windows.create_post import CreatePostWindow
from app.bot.misc.messages import delete_message


@dataclass
class CreatePostMessage:

    @staticmethod
    async def send_message_handler(message: Message, state: FSMContext) -> None:
        match message:
            case message if message.text:
                photo = None
                text = message.text
            case message if message.photo:
                photo = message.photo[-1].file_id
                text = message.caption
            case _:
                text, photo = None, None

        if text:
            await state.update_data(photo=photo, text=text)
            await CreatePostWindow.send_buttons(state, message=message)
        else:
            text = "<b>Отправьте текст или фото:</b>"
            await CreatePostWindow.send_message(state, message=message, text=text)

    @staticmethod
    async def send_buttons_handler(message: Message, state: FSMContext) -> None:
        match message:
            case message if message.text:
                try:
                    keyboards.generate_buttons(buttons=message.text)
                    await state.update_data(buttons=message.text)
                    await CreatePostWindow.choose_channel(state, message=message)
                except (Exception,):
                    text = "<b>Отправьте кнопки следуя формату.</b>\n\n"
                    await CreatePostWindow.send_buttons(state, message=message, text=text)
            case _:
                await delete_message(message)
