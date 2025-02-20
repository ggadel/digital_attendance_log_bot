import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router_help = Router()


@router_help.message(F.text, Command("help"))
async def help(message: Message):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    await message.answer("Помощь по командам: \n\n1./start - начало работы\n1./unmarked_classes - список неотмеченных классов\n3./support - тех. поддержка")