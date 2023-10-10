import asyncio
from contextlib import suppress

from aiogram import Bot
from aiogram.utils.markdown import hitalic

from app.bot import keyboards
from app.bot.misc.createtexts import create_base_info_token_text
from app.db.mysql.manage import Database
from app.translator import translate


async def start_posts(token_id: str | int, channels_ids: list, ) -> None:
    bot = Bot.get_current()
    db: Database = bot.get("db")
    token = await db.token.get(id_=token_id)

    for channel_id in channels_ids:
        channel = await db.channel.get(id_=channel_id)

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
        except (Exception,):
            pass
        text += "\n\n<b>Scan result:</b>\n"

        with suppress(Exception):
            await bot.send_message(channel_id, text, reply_markup=markup)
        await asyncio.sleep(1)


async def send_posts(channels_ids: list, text: str, photo: str = None, buttons: str = None) -> None:
    bot: Bot = Bot.get_current()
    db: Database = bot.get("db")

    for channel_id in channels_ids:
        channel = await db.channel.get(id_=channel_id)

        try:
            if channel.language_code != "ru":
                translated_text = await translate(text, 'ru', channel.language_code)
            else:
                translated_text = text
            markup = keyboards.generate_buttons(buttons) if buttons else None

            if photo:
                await bot.send_photo(channel_id, photo, caption=translated_text, reply_markup=markup)
            else:
                await bot.send_message(channel_id, translated_text, reply_markup=markup)

        except (Exception,):
            ...

        finally:
            await asyncio.sleep(1)
