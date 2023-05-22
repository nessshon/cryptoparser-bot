import json
import logging
from contextlib import suppress

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import (BotBlocked, ChatNotFound, InvalidQueryID,
                                      MessageToEditNotFound, MessageCantBeEdited, MessageNotModified,
                                      MessageToDeleteNotFound, MessageCantBeDeleted, MessageIsTooLong)
from aiogram.utils.markdown import hcode, hbold

from app.config import Config


async def errors_handler(update: Update, exception: Exception) -> bool:
    """
    Exceptions handler. Catches all exceptions within task factory tasks

    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, ChatNotFound):
        # logging.exception(f'ChatNotFound: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, BotBlocked):
        # logging.exception(f'BotBlocked: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, InvalidQueryID):
        # logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageIsTooLong):
        # logging.exception(f'MessageIsTooLong: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        # logging.exception(f'MessageToDeleteNotFound: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        # logging.exception(f'MessageCantBeDeleted: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageToEditNotFound):
        # logging.exception(f'MessageToEditNotFound: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageCantBeEdited):
        # logging.exception(f'MessageCantBeEdited: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageNotModified):
        # logging.exception(f'MessageNotModified: {exception} \nUpdate: {update}')
        return True

    with suppress(ChatNotFound, BotBlocked):
        config: Config = update.bot.get("config")

        await update.bot.send_message(
            chat_id=config.DEV_ID,
            text="#ERROR\n\n<b>Update:</b>\n{update}\n\n<b>Exception:</b>\n{exception}".format(
                update=hcode(json.dumps(json.loads(update.as_json()),
                                        ensure_ascii=False,
                                        sort_keys=True,
                                        indent=1)),
                exception=hbold(exception)
            )
        )

    logging.exception(f'Update: {update} \n{exception}')
    return True


def register(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
