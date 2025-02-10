import datetime
import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.database.queries import DataBase

from loader import bot


router_get_codes = Router()


@router_get_codes.message(F.text, Command("get_codes"))
async def get_codes(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    result = await DataBase.get_codes()
    if len(result) == 0:
        await message.answer("Кодов не существует")
        return
    formatted_msg = []
    bot_info = await bot.get_me()
    for row in result:
        formatted_str = f"<pre><code> id кода: {row[0]}\n Код: <code>{f"https://t.me/{bot_info.username}?start={row[1]}"}</code>\n name: {row[2]}\n creater_tg_id: <code>{row[3]}</code>\n created_at: {row[4]}\n</code></pre>"
        formatted_msg.append(formatted_str)
    await message.answer(f"Коды активации:\n\n{"\n".join(formatted_msg)}")