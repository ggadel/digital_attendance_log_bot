import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.database.queries import DataBase


router_remove_code = Router()


@router_remove_code.message(F.text, Command("remove_code"))
async def remove_code(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    try:
        code_id = int(command.args)
        await DataBase.remove_code(id=code_id)
        await message.answer(f"Код с id:<code>{command.args}</code> удалена")
    except:
        await message.answer("Ошибка: Неверно переданы аргменты. Введите <code>/remove_code [айди записи]</code>")