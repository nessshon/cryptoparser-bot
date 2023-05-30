import logging
from contextlib import suppress

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hide_link
from sqlalchemy import exc

from app.config import Config
from app.db.sqlite.manage import Database
from app.db.sqlite.models import Token
from parser.coingecko import get_social_links, get_new_tokens
from parser.cryptach import get_screenshot_link


async def parse(db: Database, bot: Bot, config: Config) -> None:
    screenshot_link: None | str = None
    social_links: None | dict = None
    tokens = get_new_tokens()

    def check_chain(token_: Token) -> tuple[str, str] | tuple[None, None]:
        for chain_ in token_.chains:
            if chain_.name in [token.ChainType.BSC, token.ChainType.Ethereum]:
                contract_address_ = chain_.contract_address
                chain_name_ = chain_.name
                return contract_address_, chain_name_
        return None, None

    for token in tokens:
        contract_address, chain_name = check_chain(token)

        if contract_address and chain_name:
            try:
                screenshot_link = get_screenshot_link(contract_address)
            except (Exception,):
                screenshot_link = None

        if screenshot_link:
            try:
                social_links = get_social_links(contract_address)
            except (Exception,):
                social_links = None

        if social_links:
            try:
                db_token = await db.token.add(
                    id=contract_address,
                    name=token.name,
                    chain=chain_name,
                    links=social_links,
                    screenshot_link=screenshot_link,
                )
            except exc.IntegrityError:
                db_token = None
                logging.info(f"Token {token.name} already exists")

            if db_token:
                db_admins = [admin.id for admin in await db.user.get_all_admins()]
                for admin_id in [config.ADMIN_ID, config.DEV_ID] + db_admins:
                    await send_message(bot, db_token, admin_id)

    logging.info("Parsing finished!")


async def send_message(bot: Bot, db_token: Token, chat_id: str | int) -> None:
    text = hide_link(db_token.screenshot_link)
    text += (
        f"#ДобавленТокен\n\n"
        f"<b>Название:</b> {db_token.name}\n"
        f"<b>Сеть:</b> {db_token.chain}\n"
        f"<b>Контракт:</b> <code>{db_token.id}</code>\n"
    )
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(text="⌬ Открыть", callback_data=f"token:o{db_token.id}"),
        InlineKeyboardButton(text="× Удалить", callback_data=f"token:d{db_token.id}"),
        InlineKeyboardButton(text="⊗ Скрыть", callback_data=f"token:h{db_token.id}"),
    )
    with suppress(Exception):
        await bot.send_message(chat_id, text=text, reply_markup=markup)
