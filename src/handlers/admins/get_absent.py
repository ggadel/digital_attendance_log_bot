import datetime
import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.database.queries import DataBase


router_get_absent = Router()


@router_get_absent.message(F.text, Command("get_absent"))
async def get_absent(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    date = command.args
    try:
        date_format = "%d-%m-%Y"
        formatted_date = datetime.datetime.strptime(date, date_format)
        result = await DataBase.get_absent(date=formatted_date)
        if len(result) == 0:
            await message.answer("В этот день записи отсутствуют")
            return
        formatted_msg = []
        for row in result:
            formatted_str = f"<pre> id записи: {row[0]}\n Класс: {row[1]}\n Учащихся: {row[2]}\n Отсутствует: {row[3]}\n Отсутствующие: {row[4]}\n Добавил: {row[5]}, @{row[6]}</pre>"
            formatted_msg.append(formatted_str)
        await message.answer(f"Отмеченные классы за {formatted_date}:\n{"\n".join(formatted_msg)}")
    except:
        await message.answer("Ошибка: Неверно переданы аргменты. Введите <code>/get_absent [DD-MM-YYYY]</code>")