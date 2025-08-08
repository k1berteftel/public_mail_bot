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
    return {'admin': admin}


async def rate_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    months = int(clb.data.split('_')[0])
    if months == 1:
        price = 10
    elif months == 3:
        price = 20
    else:
        price = 30
    data = {
        'months': months,
        'amount': price
    }
    await dialog_manager.start(PaymentSG.payment_type, data=data)


async def about_getter(dialog_manager: DialogManager, **kwargs):
    text = 'Какой-то текст о боте, о подписке и так далее'
    return {'text': text}
