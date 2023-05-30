from aiogram.dispatcher.filters.state import StatesGroup, State


class MainState(StatesGroup):
    menu = State()


class AdminMenuState(StatesGroup):
    menu = State()
    add_admin = State()
    add_admin_confirm = State()
    info_admin = State()
    del_admin_confirm = State()


class ChannelMenuState(StatesGroup):
    menu = State()
    add_channel = State()
    add_channel_choose_lang = State()
    add_channel_confirm = State()
    info_channel = State()
    edit_title = State()
    edit_title_confirm = State()
    edit_lang = State()
    edit_lang_confirm = State()
    del_channel_confirm = State()


class TokenMenuState(StatesGroup):
    menu = State()
    info_token = State()
    create_post = State()
    choose_channel = State()
    choose_time = State()
    create_post_confirm = State()
    send_time = State()
    create_postpone_confirm = State()
    del_token_confirm = State()


class PostMenuState(StatesGroup):
    menu = State()
    info_post = State()
    edit_time = State()
    edit_time_confirm = State()
    edit_comment = State()
    edit_comment_confirm = State()
    del_post_confirm = State()


class CreatePostState(StatesGroup):
    send_message = State()
    send_buttons = State()
    choose_channel = State()
    send_confirm = State()
