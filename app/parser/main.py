import asyncio
import logging
import random
import traceback

from aiogram import Bot
from aiogram.utils.markdown import hitalic
from sqlalchemy import exc

from app.bot import keyboards
from app.bot.misc.createtexts import create_base_info_token_text
from app.config import Config
from app.db.mysql.manage import Database
from app.db.mysql.models import Token
from app.parser.coingecko import get_social_links, get_new_cryptocurrencies
from app.parser.cryptach import get_screenshot_link
from app.translator import translate


async def parse(db: Database, config: Config) -> None:
    screenshot_link: None | str = None
    social_links: None | dict = None
    tokens = get_new_cryptocurrencies()

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
                    screenshot=screenshot_link,
                )
            except exc.IntegrityError:
                db_token = None
                logging.info(f"Token {token.name} already exists")

            if db_token:
                await start_posts(db, config, db_token)

    logging.info("Parsing finished!")


async def start_posts(db: Database, config: Config, token: Token) -> None:
    channels = await db.channel.get_all()

    for channel in channels:
        markup = keyboards.post_buttons(token.id, token.chain)
        text = create_base_info_token_text(token)

        try:
            if token.comment:
                if channel.language_code != "ru":
                    comment = await translate(token.comment, 'ru', channel.language_code)
                else:
                    comment = token.comment
                if comment:
                    text += f"\n\n{hitalic(comment)}"
        except Exception as error:
            logging.error(traceback.format_exc())
            logging.error(error)

        bot = Bot(token=config.bot.TOKEN, parse_mode="HTML")
        try:
            await bot.send_photo(
                chat_id=channel.id,
                photo=token.screenshot,
                caption=text,
                reply_markup=markup)
            await bot.session.close()
        except (Exception,):
            ...
        finally:
            await bot.session.close()
        await asyncio.sleep(random.randint(5, 10))
