from typing import Literal

SUPPORT_LANGUAGES = {
    "ar": "Арабский",
    "zh-CN": "Китайский",
    "en": "Английский",
    "fr": "Французский",
    "de": "Немецкий",
    "it": "Итальянский",
    "ja": "Японский",
    "kk": "Казахский",
    "ko": "Корейский",
    "fa": "Персидский",
    "ru": "Русский",
    "es": "Испанский",
    "tr": "Турецкий",
    "uk": "Украинский",
    "uz": "Узбекский",
}

LanguageLiteral = Literal[
    "ar", "zh-CN", "en", "fr", "de", "it", "ja",
    "kk", "ko", "fa", "ru", "es", "tr", "uk", "uz",
]
