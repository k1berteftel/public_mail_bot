from typing import Literal
import asyncio
from asyncio import TimeoutError

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.payments.create_payment import check_crypto_payment, check_oxa_payment
from database.action_data_class import DataInteraction
from config_data.config import Config, load_config
from utils.schedulers import check_sub


config: Config = load_config()


async def wait_for_payment(
        payment_id,
        user_id: int,
        bot: Bot,
        session: DataInteraction,
        scheduler: AsyncIOScheduler,
        months: int,
        payment_type: Literal['crypto', 'cryptoBot'],
        timeout: int = 60 * 15,
        check_interval: int = 6
):
    """
    Ожидает оплаты в фоне. Завершается при оплате или по таймауту.
    """
    try:
        await asyncio.wait_for(_poll_payment(payment_id, user_id, bot, session, scheduler, months, payment_type, check_interval),
                               timeout=timeout)

    except TimeoutError:
        print(f"Платёж {payment_id} истёк (таймаут)")

    except Exception as e:
        print(f"Ошибка в фоновом ожидании платежа {payment_id}: {e}")


async def _poll_payment(payment_id, user_id: int, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler, months: int, payment_type: str, interval: int):
    """
    Цикл опроса статуса платежа.
    Завершается, когда платёж оплачен.
    """
    while True:
        if payment_type == 'crypto':
            status = await check_oxa_payment(payment_id)
        else:
            status = await check_crypto_payment(payment_id)
        if status:
            await bot.send_message(
                chat_id=user_id,
                text='✅Оплата прошла успешно'
            )
            await execute_rate(user_id, bot, session, scheduler, months)
            break
        await asyncio.sleep(interval)


async def execute_rate(user_id: int, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler, months: int):
    new = await session.update_user_sub(user_id, months)
    if new:
        job_id = f'check_sub_{user_id}'
        scheduler.add_job(
            check_sub,
            'interval',
            args=[bot, user_id, session, scheduler],
            id=job_id,
            days=1
        )
        text = '✅Подписка была успешна активирована, чтобы начать пользоваться функциями бота введите команду /start'
    else:
        text = '✅Подписка была успешно продлена'
    await bot.send_message(
        chat_id=user_id,
        text=text
    )
