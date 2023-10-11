from aiogram.utils.markdown import hide_link

from app.db.mysql.models import Token


def create_base_info_token_text(token: Token) -> str:
    links = "\n".join(f"<b>{key}:</b> {val}" for key, val in token.links.items())

    text = (
        f"<b>Token</b> {token.name}\n"
        f"<b>In:</b> {token.chain}\n\n"
        f"<b>Contract:</b>\n<code>{token.id}</code>\n"
        f"{links}"
    )
    return text


def create_info_token_text(token: Token) -> str:
    text = create_base_info_token_text(token)
    text += f"\n\n<i>{token.comment}</i>" if token.comment else ""
    return text
