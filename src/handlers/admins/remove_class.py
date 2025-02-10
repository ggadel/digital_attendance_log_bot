import json
import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.data.config import PATH_TO_LIST_OF_CLASSES


router_remove_class = Router()


@router_remove_class.message(F.text, Command("remove_class"))
async def remove_class(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    classes_names = command.args
    if classes_names is None:
        await message.answer("Ошибка: Неверно переданы аргменты. Введите <code>/remove_class [класс]</code> или <code>/remove_class [класс1, класс2]</code>")
        return
    split_args = classes_names.split(",")
    with open(PATH_TO_LIST_OF_CLASSES, 'r') as f:
        list_of_classes = json.load(f)
        removed_classes = []
        for obj in split_args:
            obj = obj.replace(" ", "").lower()
            if obj in list_of_classes:
                list_of_classes.remove(obj)
                removed_classes.append(obj)
        with open(PATH_TO_LIST_OF_CLASSES, 'w') as f:
            json.dump((list_of_classes), f)
        await message.answer(f"Удалены классы: {removed_classes}")