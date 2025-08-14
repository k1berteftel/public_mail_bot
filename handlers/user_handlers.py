from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.schedulers import check_sub
from database.action_data_class import DataInteraction
from states.state_groups import startSG, SubSG


user_router = Router()


@user_router.message(CommandStart())
async def start_dialog(msg: Message, dialog_manager: DialogManager, session: DataInteraction, scheduler: AsyncIOScheduler, command: CommandObject):
    args = command.args
    referral = None
    if args:
        link_ids = await session.get_links()
        ids = [i.link for i in link_ids]
        if args in ids:
            await session.add_admin(msg.from_user.id, msg.from_user.full_name)
            await session.del_link(args)
        if not await session.check_user(msg.from_user.id):
            deeplinks = await session.get_deeplinks()
            deep_list = [i.link for i in deeplinks]
            if args in deep_list:
                await session.add_entry(args)
            try:
                args = int(args)
                users = [user.user_id for user in await session.get_users()]
                if args in users:
                    referral = args
                    #await session.add_refs(args)
            except Exception as err:
                print(err)
    await session.add_user(msg.from_user.id, msg.from_user.username if msg.from_user.username else 'Отсутствует',
                           msg.from_user.full_name, referral)
    if dialog_manager.has_context():
        await dialog_manager.done()
        try:
            await msg.bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id - 1)
        except Exception:
            ...
    user = await session.get_user(msg.from_user.id)
    if user.sub:
        job_id = f'check_sub_{user.user_id}'
        job = scheduler.get_job(job_id)
        if not job:
            scheduler.add_job(
                check_sub,
                'interval',
                args=[msg.bot, msg.from_user.id, session, scheduler],
                id=job_id,
                days=1
            )
        await dialog_manager.start(SubSG.start, mode=StartMode.RESET_STACK)
        return
    await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)
