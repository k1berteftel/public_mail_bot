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
