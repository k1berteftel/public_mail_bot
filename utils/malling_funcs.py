import asyncio

from aiogram import Bot
from pyrogram import Client

from config_data.config import load_config, Config


config: Config = load_config()


async def process_malling(account: str, base: list[str], user_id: int, msg_id: int, chat_id: int, bot: Bot):
    client = Client(f'account/{user_id}_{account}', api_id=config.user_bot.api_id, api_hash=config.user_bot.api_hash)
    try:
        await client.start()
    except Exception:
        await bot.send_message(
            chat_id=user_id,
            text='❗️Сессия вашего аккаунта слетела, пожалуйста удалите и добавьте в бота данный аккаунт повторно'
        )
    counter = 0
    for user in base:
        try:
            await client.copy_message(
                chat_id=user,
                from_chat_id=chat_id,
                message_id=msg_id
            )
            counter += 1
        except Exception as err:
            print(err)
            await asyncio.sleep(30)
        await asyncio.sleep(10)

    if client.is_connected:
        await client.stop()
    await bot.send_message(
        chat_id=user_id,
        text=f'Рассылка прошла успешно!\n\nСообщение получило <em>{counter}</em> пользователей'
    )
