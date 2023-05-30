from aiogram import Dispatcher

from app.bot.filters import IsAdmin, IsPrivate


def register(dp: Dispatcher) -> None:
    from app.bot.states import AdminMenuState
    from app.bot.handlers.messages.admin import AdminMessage
    dp.register_message_handler(
        AdminMessage.add_admin_handler, IsAdmin(), IsPrivate(),
        state=AdminMenuState.add_admin, content_types="any",
    )

    from app.bot.states import ChannelMenuState
    from app.bot.handlers.messages.channel import ChannelMessage
    dp.register_message_handler(
        ChannelMessage.add_channel_handler, IsAdmin(), IsPrivate(),
        state=ChannelMenuState.add_channel, content_types="any",
    )
    dp.register_message_handler(
        ChannelMessage.edit_title_handler, IsAdmin(), IsPrivate(),
        state=ChannelMenuState.edit_title, content_types="any",
    )

    from app.bot.states import TokenMenuState
    from app.bot.handlers.messages.token import TokenMessage
    dp.register_message_handler(
        TokenMessage.create_post_handler, IsAdmin(), IsPrivate(),
        state=TokenMenuState.create_post, content_types="any",
    )
    dp.register_message_handler(
        TokenMessage.send_time_handler, IsAdmin(), IsPrivate(),
        state=TokenMenuState.send_time, content_types="any",
    )

    from app.bot.states import PostMenuState
    from app.bot.handlers.messages.post import PostMessage
    dp.register_message_handler(
        PostMessage.edit_time_handler, IsAdmin(), IsPrivate(),
        state=PostMenuState.edit_time, content_types="any",
    )
    dp.register_message_handler(
        PostMessage.edit_comment_handler, IsAdmin(), IsPrivate(),
        state=PostMenuState.edit_comment, content_types="any",
    )

    from app.bot.states import CreatePostState
    from app.bot.handlers.messages.create_post import CreatePostMessage
    dp.register_message_handler(
        CreatePostMessage.send_message_handler, IsAdmin(), IsPrivate(),
        state=CreatePostState.send_message, content_types="any",
    )
    dp.register_message_handler(
        CreatePostMessage.send_buttons_handler, IsAdmin(), IsPrivate(),
        state=CreatePostState.send_buttons, content_types="any",
    )
