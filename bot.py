import asyncio
import logging
import os
import inspect
import pytz
import datetime

import uvicorn
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.pay_application import router
from storage.nats_storage import NatsStorage
from utils.nats_connect import connect_to_nats
from database.build import PostgresBuild
from database.action_data_class import DataInteraction
from database.model import Base
from config_data.config import load_config, Config
from handlers.user_handlers import user_router
from handlers.payment_handlers import payment_router
from dialogs import get_dialogs
from middlewares import TransferObjectsMiddleware, RemindMiddleware


timezone = pytz.timezone('Europe/Moscow')
datetime.datetime.now(timezone)

module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))


format = '[{asctime}] #{levelname:8} {filename}:' \
         '{lineno} - {name} - {message}'

logging.basicConfig(
    level=logging.DEBUG,
    format=format,
    style='{'
)


logger = logging.getLogger(__name__)

config: Config = load_config()


async def run_aiogram():
    database = PostgresBuild(config.db.dns)
    #await database.drop_tables(Base)
    #await database.create_tables(Base)
    session = database.session()
    db = DataInteraction(session)
    #await db.update_user_sub(7830831839, 1)

    scheduler: AsyncIOScheduler = AsyncIOScheduler()
    scheduler.start()

    #nc, js = await connect_to_nats(servers=config.nats.servers)
    #storage: NatsStorage = await NatsStorage(nc=nc, js=js).create_storage()

    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()#storage=storage)

    # подключаем роутеры
    dp.include_routers(user_router, payment_router, *get_dialogs())

    # подключаем middleware
    dp.update.middleware(TransferObjectsMiddleware())
    dp.update.middleware(RemindMiddleware())

    # запуск
    await bot.delete_webhook(drop_pending_updates=True)
    setup_dialogs(dp)
    logger.info('Bot start polling')

    try:
        await dp.start_polling(bot, _session=session, _scheduler=scheduler)
    except Exception as e:
        logger.exception(e)
    finally:
        #await nc.close()
        logger.info('Connection closed')


async def run_uvicorn():
    app = FastAPI()
    app.include_router(router)

    config = uvicorn.Config(app, host='0.0.0.0', port=8000, log_level="info")  # ssl_keyfile='ssl/key.pem', ssl_certfile='ssl/cert.pem'
    server = uvicorn.Server(config)
    try:
        await server.serve()
    except Exception as err:
        logger.exception(err)
    finally:
        await server.shutdown()


async def main():
    await asyncio.gather(
        run_aiogram(),
        run_uvicorn()
    )


if __name__ == "__main__":
    asyncio.run(main())