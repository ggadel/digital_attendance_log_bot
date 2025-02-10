import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.database.queries import DataBase


router_remove_permission = Router()


@router_remove_permission.message(F.text, Command("remove_permission"))
async def remove_permission(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    try:
        user_tg_id = int(command.args)
        if await DataBase.get_user(user_tg_id=user_tg_id) == "User not found":
            await message.answer(f"Пользователь id:<code>{command.args}</code> не найден")
            return
        else:
            await DataBase.remove_mark_permission(user_tg_id=user_tg_id)
            await message.answer(f"Пользователь id:<code>{command.args}</code> потерял разрешение отмечать отсутствующих")
    except:
        await message.answer("Ошибка: Неверно переданы аргменты. Введите <code>/remove_permission [айди пользователя]</code>")