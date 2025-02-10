import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.database.queries import DataBase


router_remove_entry = Router()


@router_remove_entry.message(F.text, Command("remove_entry"))
async def remove_entry(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    try:
        entry_id = int(command.args)
        await DataBase.remove_entry(id=entry_id)
        await message.answer(f"Запись с id:<code>{command.args}</code> удалена")
    except:
        await message.answer("Ошибка: Неверно переданы аргменты. Введите <code>/remove_entry [айди записи]</code>")