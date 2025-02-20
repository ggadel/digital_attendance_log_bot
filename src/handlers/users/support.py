import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from src.data.config import DEVLOPER_USER_NAME

router_support = Router()


@router_support.message(F.text, Command("support"))
async def support(message: Message):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    await message.answer(f"Возник вопрос или нашли ошибку? Пишите - @{DEVLOPER_USER_NAME}")