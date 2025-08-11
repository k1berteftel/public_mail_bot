from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, PaymentSG


config: Config = load_config()


async def start_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    admin = False
    admins = [*config.bot.admin_ids]
    admins.extend([admin.user_id for admin in await session.get_admins()])
    if event_from_user.id in admins:
        admin = True
    text = ('<b>🤚Тебя приветсвует «Твой Рассыльщик»! </b>\n\n🤖 Этот бот создан для тех, кто занимается '
            'телеграм-рассылками. С его помощью вы сможете автоматизировать отправку сообщений через ваши '
            'личные аккаунты Telegram прямо в собранную вами базу, экономя при этом кучу времени и усилий.\n\n'
            '<b>💡 Зачем это нужно?</b>\nБот полностью автоматизирует процесс рассылок, освобождая ваше время для '
            'более важных задач. Больше никакой ручной работы — все быстро, удобно и эффективно.\n\n<em>🌟 Начните '
            'использовать «Вашего Рассыльщика» уже сегодня и почувствуйте, как ваша работа становится проще и '
            'продуктивнее!</em>')
    return {
        'text': text,
        'admin': admin
    }


async def rate_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    months = int(clb.data.split('_')[0])
    if months == 1:
        price = 1000
    elif months == 3:
        price = 2000
    else:
        price = 3000
    data = {
        'months': months,
        'amount': price
    }
    await dialog_manager.start(PaymentSG.payment_type, data=data)


async def about_getter(dialog_manager: DialogManager, **kwargs):
    text = ('🤖 <b>«Твой Рассыльщик»</b> — это мощный инструмент для автоматизации рассылок в Telegram. '
            'Бот создан специально для тех, кто хочет сэкономить время и сделать процесс отправки сообщений '
            'максимально эффективным.\n\n<b>📌 Как это работает?</b>\n1️⃣ Подключите свои личные аккаунты Telegram.'
            '2️⃣ Добавьте базу контактов для рассылки (до 50 пользователей).\n3️⃣ Создайте сообщение для рассылки: '
            'текст, изображения.\n4️⃣ Запустите рассылку — бот сделает все за вас.\n\n🎯 Какую пользу вы получите?\n'
            'Бот берет на себя всю рутину, связанную с рассылками, освобождая ваше время для решения более '
            'важных задач.\n\n<b>❗️ Важно:</b>\nРассылки происходят через ваши личные аккаунты\n<b>🚀 Готовы начать? '
            'Выберите тариф и подключите бота уже сегодня!</b>')
    return {'text': text}
