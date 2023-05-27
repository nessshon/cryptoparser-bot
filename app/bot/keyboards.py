from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.config import Config
from app.db.sqlite.models import Channel, User, Token
from app.translator import SUPPORT_LANGUAGES


class CallbackData:
    ADD = 'add'
    ALL = 'all'
    SKIP = 'skip'
    BACK = 'back'
    NEXT = 'next'
    START = 'start'
    DELETE = 'delete'
    CONFIRM = 'confirm'
    POSTPONE = 'postpone'

    ADMINS = 'admins'
    CHANNELS = 'channels'

    TOKENS = 'tokens'
    PENDING = 'pending'

    MAKE_POST = 'make_post'
    EDIT_TITLE = 'edit_title'
    EDIT_LANGUAGE = "edit_language"

    EDIT_TIME = 'edit_time'
    EDIT_COMMENT = 'edit_comment'


def post_buttons(token_id: str, chain: str) -> InlineKeyboardMarkup:
    from parser.coingecko.new_cryptocurrencies import Token

    if chain == Token.ChainType.Ethereum:
        explorer_text = "Etherscan"
        explorer_url = f"https://etherscan.io/token/{token_id}"
        swap_url = f"https://pancakeswap.finance/swap?chain=eth&outputCurrency={token_id}"
    else:
        explorer_text = "BSCscan"
        explorer_url = f"https://bscscan.com/token/{token_id}"
        swap_url = f"https://pancakeswap.finance/swap?chain=bsc&outputCurrency={token_id}"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="PancakeSwap", url=swap_url),
                InlineKeyboardButton(text=explorer_text, url=explorer_url)
            ]
        ]
    )


def choose_time() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="★ Отложить", callback_data=CallbackData.POSTPONE),
                InlineKeyboardButton(text="► Запустить", callback_data=CallbackData.START),
            ],
            [
                InlineKeyboardButton(text="‹ Назад", callback_data=CallbackData.BACK),
            ],
        ]
    )


def post_info():
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton(text="✎ Изменить время", callback_data=CallbackData.EDIT_TIME),
        InlineKeyboardButton(text="✎ Изменить комментарий", callback_data=CallbackData.EDIT_COMMENT),

    )
    markup.row(
        InlineKeyboardButton(text="‹ Назад", callback_data=CallbackData.BACK),
        InlineKeyboardButton(text="× Удалить", callback_data=CallbackData.DELETE),
    )
    return markup


def post_menu(posts: list[tuple]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        *[
            InlineKeyboardButton(text=post[0], callback_data=post[1])
            for post in posts
        ]
    )
    markup.row(
        InlineKeyboardButton(text="‹ Назад", callback_data=CallbackData.BACK),
    )
    return markup


def token_info() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✎ Оформить пост", callback_data=CallbackData.MAKE_POST)
            ],
            [
                InlineKeyboardButton(text="‹ Назад", callback_data=CallbackData.BACK),
                InlineKeyboardButton(text="× Удалить", callback_data=CallbackData.DELETE),
            ],
        ]
    )


def token_menu(tokens: list[Token]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        *[
            InlineKeyboardButton(text=token.name, callback_data=str(token.id))
            for token in tokens
        ]
    )
    markup.row(
        InlineKeyboardButton(text='‹ Назад', callback_data=CallbackData.BACK),
    )
    return markup


def channel_info() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✎ Изменить язык", callback_data=CallbackData.EDIT_LANGUAGE)],
            [InlineKeyboardButton(text="✎ Изменить название", callback_data=CallbackData.EDIT_TITLE)],
            [
                InlineKeyboardButton(text="‹ Назад", callback_data=CallbackData.BACK),
                InlineKeyboardButton(text="× Удалить", callback_data=CallbackData.DELETE),
            ],
        ]
    )


def channel_menu(channels: list[Channel]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        *[
            InlineKeyboardButton(text=channel.title, callback_data=str(channel.id))
            for channel in channels
        ]
    )
    markup.row(
        InlineKeyboardButton(text='‹ Назад', callback_data=CallbackData.BACK),
        InlineKeyboardButton(text='+ Добавить', callback_data=CallbackData.ADD),
    )
    return markup


def admin_info() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="‹ Назад", callback_data=CallbackData.BACK),
                InlineKeyboardButton(text="× Удалить", callback_data=CallbackData.DELETE),
            ]
        ]
    )


def admin_menu(admins: list[User]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        *[
            InlineKeyboardButton(text=admin.first_name, callback_data=str(admin.id))
            for admin in admins if admins
        ]
    )
    markup.row(
        InlineKeyboardButton(text='‹ Назад', callback_data=CallbackData.BACK),
        InlineKeyboardButton(text='+ Добавить', callback_data=CallbackData.ADD),
    )
    return markup


def added_channels(channels: list[Channel]) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        *[
            InlineKeyboardButton(text=channel.title, callback_data=str(channel.id))
            for channel in channels
        ]
    )
    markup.row(
        InlineKeyboardButton(text='‹ Назад', callback_data=CallbackData.BACK)
    )
    return markup


def choose_channels(channels: list[Channel], selected: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(text='≣ Выбрать все', callback_data=CallbackData.ALL)
    )
    markup.add(
        *[
            InlineKeyboardButton(
                text=f"🟢 {channel.title}" if channel.id in selected else f"🔘 {channel.title}",
                callback_data=str(channel.id)
            )
            for channel in channels
        ]
    )
    markup.row(
        InlineKeyboardButton(text='‹ Назад', callback_data=CallbackData.BACK),
        InlineKeyboardButton(text='Далее ›', callback_data=CallbackData.NEXT),
    )
    return markup


def support_languages() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        *[
            InlineKeyboardButton(text=text, callback_data=callback_data)
            for callback_data, text in SUPPORT_LANGUAGES.items()
        ]
    )
    markup.row(
        InlineKeyboardButton(text="‹ Назад", callback_data=CallbackData.BACK),
    )
    return markup


def main_menu(config: Config, user_id: int | str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(text="🪙 Токены", callback_data=CallbackData.TOKENS),
        InlineKeyboardButton(text="🕝 Отложено", callback_data=CallbackData.PENDING),
    )
    if int(user_id) in [config.ADMIN_ID, config.DEV_ID]:
        markup.add(
            InlineKeyboardButton(text="📢 Каналы", callback_data=CallbackData.CHANNELS),
            InlineKeyboardButton(text="👤 Админы", callback_data=CallbackData.ADMINS),
        )
    return markup


def back_confirm() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='‹ Назад', callback_data=CallbackData.BACK),
                InlineKeyboardButton(text='✓ Подтвердить', callback_data=CallbackData.CONFIRM),
            ]
        ]
    )


def back_skip() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='‹ Назад', callback_data=CallbackData.BACK),
                InlineKeyboardButton(text='Пропустить ›', callback_data=CallbackData.SKIP),
            ]
        ]
    )


def back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='‹ Назад', callback_data=CallbackData.BACK)],
        ]
    )
