from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.user_dialog import getters
from states.state_groups import startSG, adminSG

user_dialog = Dialog(
    Window(
        Format('{text}'),
        Column(
            SwitchTo(Const('👑Выбрать тариф'), id='rate_choose_switcher', state=startSG.rate_choose),
            SwitchTo(Const('ℹ️О боте'), id='about_switcher', state=startSG.about),
            SwitchTo(Const('📋Правила'), id='rules_switcher', state=startSG.rules),
            Url(Const('🔗Тех.поддержка'), id='tech_url', url=Const('https://t.me/Leggit_Russia')),
            Start(Const('Админ панель'), id='admin', state=adminSG.start, when='admin')
        ),
        getter=getters.start_getter,
        state=startSG.start
    ),
    Window(
        Const('⌛️Выберите тариф подписки'),
        Column(
            Button(Const('👍1 месяц (750₽)'), id='1_month_choose', on_click=getters.rate_choose),
            Button(Const('⚡️3 месяца (2000₽)'), id='3_month_choose', on_click=getters.rate_choose),
            Button(Const('🔥6 месяцев (3500₽)'), id='6_month_choose', on_click=getters.rate_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.rate_choose
    ),
    Window(
        Format('{text}'),
        SwitchTo(Const('👑Выбрать тариф'), id='rate_choose_switcher', state=startSG.rate_choose),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        getter=getters.about_getter,
        state=startSG.about
    ),
    Window(
        Const('<b>📄Правила по использованию бота</b>'),
        Column(
            Url(Const('🔗Политика конфиденциальности'), id='policy_url', url=Const('https://teletype.in/@leggit/LQXR_kR-SsG')),
            Url(Const('🔗Пользовательское соглашение'), id='rules_url', url=Const('https://teletype.in/@leggit/ku5f9EjAOKo')),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.rules
    )
)