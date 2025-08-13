import asyncio

from aiogram.types import (CallbackQuery, User, Message, InlineKeyboardButton,
                           InlineKeyboardMarkup, LabeledPrice)
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.payments.create_payment import (get_oxa_payment_data, get_crypto_payment_data,
                                           get_freekassa_card, get_freekassa_sbp)
from utils.payments.process_payment import wait_for_payment
from database.action_data_class import DataInteraction
from states.state_groups import startSG, PaymentSG
from config_data.config import load_config, Config


pay_description = {
    1: 'Покупка 1 месяца подписки',
    3: 'Покупка 3 месяцев подписки',
    6: 'Покупка 6 месяцев подписки'
}


async def payment_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    scheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('scheduler')
    months = dialog_manager.start_data.get('months')
    amount = dialog_manager.start_data.get('amount')
    payment_type = clb.data.split('_')[0]
    if payment_type == 'card':
        payment = await get_freekassa_card(clb.from_user.id, amount, months)
    elif payment_type == 'sbp':
        payment = await get_freekassa_sbp(clb.from_user.id, amount, months)
    elif payment_type == 'crypto':
        payment = await get_oxa_payment_data(amount)
        task = asyncio.create_task(
            wait_for_payment(
                payment_id=payment.get('id'),
                user_id=clb.from_user.id,
                bot=clb.bot,
                session=session,
                scheduler=scheduler,
                payment_type='crypto',
                months=months
            )
        )
        for active_task in asyncio.all_tasks():
            if active_task.get_name() == f'process_payment_{clb.from_user.id}':
                active_task.cancel()
        task.set_name(f'process_payment_{clb.from_user.id}')
    elif payment_type == 'cryptoBot':
        payment = await get_crypto_payment_data(amount)
        task = asyncio.create_task(
            wait_for_payment(
                payment_id=payment.get('id'),
                user_id=clb.from_user.id,
                bot=clb.bot,
                session=session,
                scheduler=scheduler,
                payment_type='cryptoBot',
                months=months
            )
        )
        for active_task in asyncio.all_tasks():
            if active_task.get_name() == f'process_payment_{clb.from_user.id}':
                active_task.cancel()
        task.set_name(f'process_payment_{clb.from_user.id}')
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='🔗Оплатить', pay=True)],
                [InlineKeyboardButton(text='❌Закрыть', callback_data='close_payment')]
            ]
        )
        price = int(round(amount / 1.6, 0))
        prices = [LabeledPrice(label="XTR", amount=price)]
        await clb.message.answer_invoice(
            title='Покупка подписки',
            description=pay_description[months],
            payload=str(months),
            currency="XTR",
            prices=prices,
            provider_token="",
            reply_markup=keyboard
        )
        return
    dialog_manager.dialog_data['url'] = payment.get('url')
    await dialog_manager.switch_to(PaymentSG.process_payment)


async def process_payment_getter(dialog_manager: DialogManager, **kwargs):
    url = dialog_manager.dialog_data.get('url')
    return {'url': url}


async def close_poll_payment(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    name = f'process_payment_{clb.from_user.id}'
    for task in asyncio.all_tasks():
        if task.get_name() == name:
            task.cancel()
    await dialog_manager.switch_to(PaymentSG.payment_type)



