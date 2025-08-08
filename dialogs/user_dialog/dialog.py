from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.user_dialog import getters
from states.state_groups import startSG, adminSG

user_dialog = Dialog(
    Window(
        Const('Приветственный текст'),
        Column(
            SwitchTo(Const('👑Приобрести подписку'), id='rate_choose_switcher', state=startSG.rate_choose),
            SwitchTo(Const('🔎О боте'), id='about_switcher', state=startSG.about),
            Url(Const('🔗Тех.поддержка'), id='tech_url', url=Const('https://t.me/Leggit_Russia')),
            Start(Const('Админ панель'), id='admin', state=adminSG.start, when='admin')
        ),
        getter=getters.start_getter,
        state=startSG.start
    ),
    Window(
        Const('⌛️Выберите тариф подписки'),
        Column(
            Button(Const('👍1 месяц (...₽)'), id='1_month_choose', on_click=getters.rate_choose),
            Button(Const('⚡️3 месяца (...₽)'), id='3_month_choose', on_click=getters.rate_choose),
            Button(Const('🔥6 месяцев (...₽)'), id='6_month_choose', on_click=getters.rate_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.rate_choose
    ),
    Window(
        Format('{text}'),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        getter=getters.about_getter,
        state=startSG.about
    )
)