from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.sub_dialog import getters
from states.state_groups import SubSG


sub_dialog = Dialog(
    Window(
        Format('<b>🏠Вы в главном меню</b>\n⌛️Подписка действительна до: {sub}'),
        Column(
            SwitchTo(Const('✉️Запустить рассылку'), id='choose_account_switcher', state=SubSG.choose_account),
            SwitchTo(Const('👥Управление аккаунтами'), id='accounts_switcher', state=SubSG.accounts),
            SwitchTo(Const('👑Продлить подписку'), id='rate_choose_switcher', state=SubSG.rate_choose),
            Url(Const('🔎Инструкция'), id='manual_url', url=Const('https://telegra.ph/Instrukciya-po-ispolzovaniyu-08-08-2')),
            Url(Const('🔗Тех.поддержка'), id='tech_url', url=Const('https://t.me/Leggit_Russia'))
        ),
        getter=getters.start_getter,
        state=SubSG.start
    ),
    Window(
        Const('Выберите аккаунт с которого будет воспроизводиться рассылка'),
        Group(
            Select(
                Format("{item[0]}"),
                id='choose_account_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.choose_account_selector
            ),
            width=1
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=SubSG.start),
        getter=getters.choose_account_getter,
        state=SubSG.choose_account
    ),
    Window(
        DynamicMedia('document', when='document'),
        Const('Введите юзернеймы, которым надо будет рассылать сообщение по инструкции приложенной ниже⬇️\n\n'
              '<b>❗️В базе должно быть не больше 50 человек</b>'),
        TextInput(
            id='get_usernames',
            on_success=getters.get_usernames
        ),
        MessageInput(
            func=getters.get_table_usernames,
            content_types=ContentType.DOCUMENT
        ),
        SwitchTo(Const('✅База собранна'), id='get_message_switcher', state=SubSG.get_message),
        Url(Const('📋Инструкция'), id='manual_url', url=Const('https://telegra.ph/Instrukciya-po-ispolzovaniyu-08-08-2')),
        SwitchTo(Const('⬅️Назад'), id='back_choose_account', state=SubSG.choose_account),
        getter=getters.get_usernames_getter,
        state=SubSG.get_usernames
    ),
    Window(
        Const('Отправьте сообщение, которое надо будет разослать по базе'),
        MessageInput(
            func=getters.get_message,
            content_types=ContentType.ANY
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_usernames', state=SubSG.get_usernames),
        state=SubSG.get_message
    ),
    Window(
        Const('Вы подтверждаете, рассылку сообщения по собранной базе пользователей'),
        Row(
            Button(Const('Запуск'), id='start_malling', on_click=getters.start_malling),
            Button(Const('Отмена'), id='cancel_malling', on_click=getters.cancel_malling),
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_message', state=SubSG.get_message),
        state=SubSG.confirm_malling
    ),
    Window(
        Const('⌛️Выберите тариф для продления подписки'),
        Column(
            Button(Const('👍1 месяц (...₽)'), id='1_month_choose', on_click=getters.rate_choose),
            Button(Const('⚡️3 месяца (...₽)'), id='3_month_choose', on_click=getters.rate_choose),
            Button(Const('🔥6 месяцев (...₽)'), id='6_month_choose', on_click=getters.rate_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=SubSG.start),
        state=SubSG.rate_choose
    ),
    Window(
        Format('<b>Меню привязки аккаунтов</b>\n\n{text}'),
        Column(
            SwitchTo(Const('➕Добавить аккаунт'), id='add_account', state=SubSG.get_name),
            SwitchTo(Const('🗑Удалить аккаунт'), id='del_account_switcher', state=SubSG.del_account)
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=SubSG.start),
        getter=getters.accounts_getter,
        state=SubSG.accounts
    ),
    Window(
        Const('Нажмите на аккаунт, вы хотели бы удалить👇'),
        Group(
            Select(
                Format("{item[0]}"),
                id='del_account_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.del_account_selector
            ),
            width=1
        ),
        Back(Const('⬅️Назад'), id='back_accounts'),
        getter=getters.del_account_getter,
        state=SubSG.del_account
    ),
    Window(
        Format('Вы подтверждаете удаление аккаунта <em>"{name}"</em>?'),
        Column(
            Button(Const('🗑Удалить'), id='confirm_account_del', on_click=getters.del_account),
            SwitchTo(Const('❌Отмена'), id='back_accounts', state=SubSG.accounts),
        ),
        getter=getters.del_account_confirm_getter,
        state=SubSG.del_account_confirm
    ),
    Window(
        Const('Введите название для аккаунта'),
        TextInput(
            id='get_name',
            on_success=getters.get_name
        ),
        SwitchTo(Const('⬅️Назад'), id='back_accounts', state=SubSG.accounts),
        state=SubSG.get_name
    ),
    Window(
        Const('Отправьте номер телефона'),
        SwitchTo(Const('Отмена'), id='back', state=SubSG.start),
        TextInput(
            id='get_phone',
            on_success=getters.phone_get,
        ),
        Back(Const('⬅️Назад'), id='back_get_name'),
        state=SubSG.add_account
    ),
    Window(
        Const('Введи код который пришел на твой аккаунт в телеграмм в формате: 1-2-3-5-6'),
        TextInput(
            id='get_kod',
            on_success=getters.get_kod,
        ),
        state=SubSG.kod_send
    ),
    Window(
        Const('Пароль от аккаунта телеграмм'),
        TextInput(
            id='get_password',
            on_success=getters.get_password,
        ),
        state=SubSG.get_password
    ),
)
