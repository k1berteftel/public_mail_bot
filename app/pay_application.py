import datetime
import json

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import APIRouter, Request, Form, FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.build import PostgresBuild
from database.action_data_class import DataInteraction
from utils.schedulers import check_sub
from config_data.config import load_config, Config


config: Config = load_config()

router = APIRouter()

database = PostgresBuild(config.db.dns)
sessions = database.session()


@router.post("/payment")
async def ping(response: Request, us_months: str = Form(...),
               us_userId: str | int = Form(...), CUR_ID: str | int = Form(...)):
    print(response.__dict__)
    user_id = int(us_userId)
    months = int(us_months)
    session = DataInteraction(sessions)
    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    new = await session.update_user_sub(user_id, months)
    if new:
        text = '✅Подписка была успешна активирована, чтобы начать пользоваться функциями бота введите команду /start'
    else:
        text = '✅Подписка была успешно продлена'
    await bot.send_message(
        chat_id=user_id,
        text=text
    )
    return "OK"