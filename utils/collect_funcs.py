import logging
from aiogram import Bot
from pyrogram import Client
from pyrogram.enums.chat_type import ChatType

from config_data.config import load_config, Config


config: Config = load_config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def collect_users_base(account: str, user_id: int, channel: str | int, bot: Bot, users: list[str] | None = None) -> list[str] | None:
    if users is None:
        users = []
    try:
        app = Client(f'accounts/{user_id}_{account.replace(" ", "_")}', api_id=config.user_bot.api_id, api_hash=config.user_bot.api_hash)
    except Exception as err:
        print(err)
        await bot.send_message(
            chat_id=user_id,
            text='❗️Сессия вашего аккаунта слетела, пожалуйста удалите и добавьте в бота данный аккаунт повторно'
        )
        return
    async with app:
        new_users = []
        members = app.get_chat_members(channel)
        try:
            async for user in members:
                if user.user.username and not user.user.is_bot and not user.user.is_contact and not user.user.verification_status.is_fake and user.user.username not in users:
                    new_users.append(user.user.username)
            if len(new_users) > 30:
                users.extend(new_users)
            else:
                async for message in app.get_chat_history(channel, limit=10000):
                    user = message.from_user
                    if user and (not user.is_bot and not user.verification_status.is_fake) and user.username and user.username not in users:
                        if user.username not in new_users:
                            new_users.append(user.username)
                users.extend(new_users)
        except Exception as err:
            print(err, err.args, err.__traceback__)

    return users if users else None


async def get_channels(account: str, bot: Bot, user_id: int):
    try:
        app = Client(f'accounts/{user_id}_{account.replace(" ", "_")}', api_id=config.user_bot.api_id, api_hash=config.user_bot.api_hash)
    except Exception as err:
        print(err)
        await bot.send_message(
            chat_id=user_id,
            text='❗️Сессия вашего аккаунта слетела, пожалуйста удалите и добавьте в бота данный аккаунт повторно'
        )
        return
    dialogs = []
    async with app:
        async for dialog in app.get_dialogs():
            if dialog.chat.type not in [ChatType.BOT, ChatType.PRIVATE]:
                dialogs.append(
                    (
                        dialog.chat.title,
                        dialog.chat.id
                    )
                )
    return dialogs