import json
import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.data.config import PATH_TO_LIST_OF_CLASSES


router_list_of_classes = Router()


@router_list_of_classes.message(F.text, Command("list_of_classes"))
async def list_of_classes(message: Message):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    with open(PATH_TO_LIST_OF_CLASSES, 'r') as f:
        list_of_classes = json.load(f)
        await message.answer(f"Список классов: {", ".join(sorted(list_of_classes))}")