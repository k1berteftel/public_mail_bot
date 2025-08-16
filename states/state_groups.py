from aiogram.fsm.state import State, StatesGroup

# Обычная группа состояний


class startSG(StatesGroup):
    start = State()
    rate_choose = State()
    about = State()
    rules = State()


class SubSG(StatesGroup):
    start = State()

    rate_choose = State()

    collect_base = State()
    my_channels = State()
    choose_get_type = State()

    choose_account = State()
    get_usernames = State()
    get_message = State()
    confirm_malling = State()

    accounts = State()
    del_account = State()
    del_account_confirm =State()
    get_name = State()
    add_account = State()
    kod_send = State()
    get_password = State()

    rules = State()


class PaymentSG(StatesGroup):
    payment_type = State()
    process_payment = State()


class adminSG(StatesGroup):
    start = State()

    get_mail = State()
    get_time = State()
    get_keyboard = State()
    confirm_mail = State()

    deeplink_menu = State()
    deeplink_del = State()

    admin_menu = State()
    admin_del = State()
    admin_add = State()

    subs_menu = State()
    get_user_id = State()
    get_days = State()
