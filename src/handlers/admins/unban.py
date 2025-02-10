import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.database.queries import DataBase


router_unban = Router()


@router_unban.message(F.text, Command("unban"))
async def unban(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    try:
        user_tg_id = int(command.args)
        if await DataBase.get_user(user_tg_id=user_tg_id) == "User not found":
            await message.answer(f"Пользователь id:<code>{user_tg_id}</code> не найден")
            return
        else:
            await DataBase.unban_user(user_tg_id=user_tg_id)
            await message.answer(f"Пользователь id:<code>{user_tg_id}</code> разбанен")
    except:
        await message.answer("Ошибка: Неверно переданы аргменты. Введите <code>/unban [айди пользователя]</code>")