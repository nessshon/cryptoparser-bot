import logging

from aiogoogletrans import Translator

from app.translator.languages import LanguageLiteral


async def translate(text: str, from_lang: LanguageLiteral, to_lang: LanguageLiteral) -> str:
    """
    Translates the given text from one language to another using the Google Translate API.

    Args:
        text (str): The text to be translated.
        from_lang (str): The language code of the source language.
        to_lang (str): The language code of the target language.

    Returns:
        str: The translated text.

    Raises:
        Exception: If an error occurs while translating the text.

    """
    translator = Translator()

    try:
        translated = await translator.translate(
            text=text,
            dest=to_lang,
            src=from_lang
        )
        return translated.text

    except Exception as e:
        logging.error(e)

    finally:
        await translator.client.aclose()
