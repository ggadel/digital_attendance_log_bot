import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.database.queries import DataBase


router_get_user = Router()


@router_get_user.message(F.text, Command("get_user"))
async def get_user(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    user_tg_id = command.args
    try:
        int_user_tg_id = int(user_tg_id)
        get_user = await DataBase.get_user(user_tg_id=int_user_tg_id)
        if get_user == "User not found":
            await message.answer("Пользователь не найден")
            return
        formatted_msg = f"id: <code>{get_user[0]}</code>\nuser tg id: <code>{get_user[1]}</code>\nusername: @{get_user[2]}\nbanned: {get_user[3]}\nmark_permission: {get_user[4]}\n<code>permission_code_id: {get_user[5]}</code>\nregistered at:<code>{get_user[6]}</code>"
        await message.answer(f"{formatted_msg}")
    except:
        await message.answer("Ошибка: Неверно переданы аргменты. Введите <code>/get_user [айди пользователя]</code>")