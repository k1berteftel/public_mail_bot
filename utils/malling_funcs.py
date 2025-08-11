import asyncio
import logging

from pyrogram import Client
from pyrogram.errors import (
    PeerFlood,
    UserIsBlocked,
    FloodWait,
    UsernameInvalid,
    UsernameNotOccupied,
    ChatWriteForbidden,
    RPCError
)
from typing import List
from aiogram import Bot
from pyrogram.enums.parse_mode import ParseMode

from config_data.config import load_config, Config


config: Config = load_config()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_malling(account: str, base: list[str], user_id: int, text: str, bot: Bot):
    client = Client(f'accounts/{user_id}_{account.replace(" ", "_")}', api_id=config.user_bot.api_id, api_hash=config.user_bot.api_hash)
    try:
        await client.start()
    except Exception as err:
        print(err)
        await bot.send_message(
            chat_id=user_id,
            text='❗️Сессия вашего аккаунта слетела, пожалуйста удалите и добавьте в бота данный аккаунт повторно'
        )
        return
    delay = 15
    results = {
        "sent": [],
        "failed": [],
        "blocked": [],
        "not_found": [],
        "flood_wait": [],
        "invalid": [],
        "write_forbidden": []
    }
    print(base)
    print('base: ', len(base))
    for username in base:
        # Очищаем юзернейм
        clean_username = username.strip().lstrip('@')
        try:
            # Отправляем сообщение
            await client.send_message(clean_username, text)
            results["sent"].append(clean_username)
            logger.info(f"✅ Сообщение отправлено: @{clean_username}")

        except PeerFlood:
            results["not_found"].append(clean_username)
            logger.warning(f"❌ Пользователь не найден: @{clean_username}")

        except UserIsBlocked:
            results["blocked"].append(clean_username)
            logger.warning(f"🚫 Пользователь заблокировал бота: @{clean_username}")

        except UsernameInvalid:
            results["invalid"].append(username)
            logger.warning(f"⚠️ Неверный формат юзернейма: {username}")

        except UsernameNotOccupied:
            results["not_found"].append(clean_username)
            logger.warning(f"❌ Юзернейм не занят: @{clean_username}")

        except ChatWriteForbidden:
            results["write_forbidden"].append(clean_username)
            logger.warning(f"⛔ Нет прав на отправку: @{clean_username}")

        except FloodWait as e:
            # Важно: нужно подождать указанное время
            wait_seconds = e.value
            logger.error(f"⏱️ FloodWait: ждём {wait_seconds} секунд...")
            await asyncio.sleep(wait_seconds)
            # Можно повторить попытку, но лучше остановиться
            results["flood_wait"].append({"username": clean_username, "wait": wait_seconds})
            break  # Прерываем, чтобы не продолжать после большого wait

        except RPCError as e:
            results["failed"].append({"username": clean_username, "error": str(e)})
            logger.error(f"❌ RPC ошибка при отправке @{clean_username}: {e}")

        except Exception as e:
            results["failed"].append({"username": clean_username, "error": str(e)})
            logger.error(f"❌ Неизвестная ошибка с @{clean_username}: {e}")

        # Задержка между сообщениями
        await asyncio.sleep(delay)
    await client.stop()
    print("📬 Рассылка завершена")
    print(f"✅ Успешно: {len(results['sent'])}")
    print(f"🚫 Заблокировали: {len(results['blocked'])}")
    print(f"❌ Не найдены: {len(results['not_found'])}")
    print(f"⏸️ FloodWait: {len(results['flood_wait'])}")
    await bot.send_message(
        chat_id=user_id,
        text=f'Рассылка прошла успешно!\n\nСообщение получило <em>{len(results["sent"])}</em> пользователей'
    )
    return results
