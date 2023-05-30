from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from app.bot.filters import IsPrivate, IsAdmin


def register(dp: Dispatcher) -> None:
    from app.bot.states import MainState
    from app.bot.handlers.callbacks.main import MainCallback
    dp.register_callback_query_handler(
        MainCallback.handler, IsPrivate(), IsAdmin(),
        Text(startswith="token:"), state="*",
    )
    dp.register_callback_query_handler(
        MainCallback.menu_handler, IsPrivate(), IsAdmin(),
        state=MainState.menu,
    )

    from app.bot.states import AdminMenuState
    from app.bot.handlers.callbacks.admin import AdminCallback
    dp.register_callback_query_handler(
        AdminCallback.menu_handler, IsPrivate(), IsAdmin(),
        state=AdminMenuState.menu,
    )
    dp.register_callback_query_handler(
        AdminCallback.add_admin_handler, IsPrivate(), IsAdmin(),
        state=AdminMenuState.add_admin,
    )
    dp.register_callback_query_handler(
        AdminCallback.add_admin_confirm_handler, IsPrivate(), IsAdmin(),
        state=AdminMenuState.add_admin_confirm,
    )
    dp.register_callback_query_handler(
        AdminCallback.info_admin_handler, IsPrivate(), IsAdmin(),
        state=AdminMenuState.info_admin,
    )
    dp.register_callback_query_handler(
        AdminCallback.del_admin_confirm_handler, IsPrivate(), IsAdmin(),
        state=AdminMenuState.del_admin_confirm,
    )

    from app.bot.states import ChannelMenuState
    from app.bot.handlers.callbacks.channel import ChannelCallback
    dp.register_callback_query_handler(
        ChannelCallback.menu_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.menu,
    )
    dp.register_callback_query_handler(
        ChannelCallback.add_channel_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.add_channel,
    )
    dp.register_callback_query_handler(
        ChannelCallback.add_channel_choose_lang_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.add_channel_choose_lang,
    )
    dp.register_callback_query_handler(
        ChannelCallback.add_channel_confirm_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.add_channel_confirm,
    )
    dp.register_callback_query_handler(
        ChannelCallback.add_channel_confirm_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.add_channel_confirm,
    )
    dp.register_callback_query_handler(
        ChannelCallback.info_channel_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.info_channel,
    )
    dp.register_callback_query_handler(
        ChannelCallback.del_channel_confirm_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.del_channel_confirm,
    )
    dp.register_callback_query_handler(
        ChannelCallback.edit_title_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.edit_title,
    )
    dp.register_callback_query_handler(
        ChannelCallback.edit_title_confirm_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.edit_title_confirm,
    )
    dp.register_callback_query_handler(
        ChannelCallback.edit_lang_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.edit_lang,
    )
    dp.register_callback_query_handler(
        ChannelCallback.edit_lang_confirm_handler, IsPrivate(), IsAdmin(),
        state=ChannelMenuState.edit_lang_confirm,
    )

    from app.bot.states import TokenMenuState
    from app.bot.handlers.callbacks.token import TokenCallback
    dp.register_callback_query_handler(
        TokenCallback.menu_handler, IsPrivate(), IsAdmin(),
        state=TokenMenuState.menu,
    )
    dp.register_callback_query_handler(
        TokenCallback.info_token_handler, IsPrivate(), IsAdmin(),
        state=TokenMenuState.info_token,
    )
    dp.register_callback_query_handler(
        TokenCallback.create_post_handler, IsPrivate(), IsAdmin(),
        state=TokenMenuState.create_post,
    )
    dp.register_callback_query_handler(
        TokenCallback.choose_channel_handler, IsPrivate(), IsAdmin(),
        state=TokenMenuState.choose_channel,
    )
    dp.register_callback_query_handler(
        TokenCallback.choose_time_handler, IsPrivate(), IsAdmin(),
        state=TokenMenuState.choose_time,
    )
    dp.register_callback_query_handler(
        TokenCallback.create_post_confirm_handler, IsPrivate(), IsAdmin(),
        state=TokenMenuState.create_post_confirm,
    )
    dp.register_callback_query_handler(
        TokenCallback.send_time_handler, IsPrivate(), IsAdmin(),
        state=TokenMenuState.send_time,
    )
    dp.register_callback_query_handler(
        TokenCallback.create_postpone_confirm_handler, IsPrivate(), IsAdmin(),
        state=TokenMenuState.create_postpone_confirm,
    )
    dp.register_callback_query_handler(
        TokenCallback.del_token_confirm_handler, IsPrivate(), IsAdmin(),
        state=TokenMenuState.del_token_confirm,
    )

    from app.bot.states import PostMenuState
    from app.bot.handlers.callbacks.post import PostCallback
    dp.register_callback_query_handler(
        PostCallback.menu_handler, IsPrivate(), IsAdmin(),
        state=PostMenuState.menu,
    )
    dp.register_callback_query_handler(
        PostCallback.info_post_handler, IsPrivate(), IsAdmin(),
        state=PostMenuState.info_post,
    )
    dp.register_callback_query_handler(
        PostCallback.edit_time_handler, IsPrivate(), IsAdmin(),
        state=PostMenuState.edit_time,
    )
    dp.register_callback_query_handler(
        PostCallback.edit_time_confirm_handler, IsPrivate(), IsAdmin(),
        state=PostMenuState.edit_time_confirm,
    )
    dp.register_callback_query_handler(
        PostCallback.edit_comment_handler, IsPrivate(), IsAdmin(),
        state=PostMenuState.edit_comment,
    )
    dp.register_callback_query_handler(
        PostCallback.edit_comment_confirm_handler, IsPrivate(), IsAdmin(),
        state=PostMenuState.edit_comment_confirm,
    )
    dp.register_callback_query_handler(
        PostCallback.del_post_confirm_handler, IsPrivate(), IsAdmin(),
        state=PostMenuState.del_post_confirm,
    )

    from app.bot.states import CreatePostState
    from app.bot.handlers.callbacks.create_post import CreatePostCallback
    dp.register_callback_query_handler(
        CreatePostCallback.send_message_handler, IsPrivate(), IsAdmin(),
        state=CreatePostState.send_message,
    )
    dp.register_callback_query_handler(
        CreatePostCallback.send_buttons_handler, IsPrivate(), IsAdmin(),
        state=CreatePostState.send_buttons,
    )
    dp.register_callback_query_handler(
        CreatePostCallback.choose_channel_handler, IsPrivate(), IsAdmin(),
        state=CreatePostState.choose_channel,
    )
    dp.register_callback_query_handler(
        CreatePostCallback.send_confirm_handler, IsPrivate(), IsAdmin(),
        state=CreatePostState.send_confirm,
    )
