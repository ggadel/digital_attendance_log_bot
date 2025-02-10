import logging
import json
import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.data.config import PATH_TO_LIST_OF_CLASSES
from src.database.queries import DataBase

router_unmarked_classes = Router()


@router_unmarked_classes.message(F.text, Command("unmarked_classes"))
async def unmarked_classes(message: Message):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    with open(PATH_TO_LIST_OF_CLASSES, 'r') as f:
        current_date = datetime.date.today()
        list_of_classes = json.load(f)
        marked_classes = await DataBase.get_absent(date=current_date)
        for list_absent in marked_classes:
            if list_absent[1] in list_of_classes:
                list_of_classes.remove(list_absent[1])
        await message.answer(f"Список не отмеченных классов: {", ".join(list_of_classes)}")