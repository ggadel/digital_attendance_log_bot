import datetime
import logging
import random
import string

from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from src.database.queries import DataBase

from src.keyboards.create_code import create_code_kb

from loader import bot


router_create_code = Router()


@router_create_code.message(F.text, Command("create_code"))
async def create_code(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    if command.args is None:
        await message.answer("Ошибка: Неверно переданы аргменты. Введите <code>/create_code [название]</code>")
        return
    global name
    name = command.args
    await message.answer(f"Создать код с названием: {name}", reply_markup=create_code_kb())


@router_create_code.callback_query(F.data == "create_code")
async def confirm_create_code(callback: types.CallbackQuery):
    code_range = string.ascii_letters + string.digits
    permission_code = ''.join(random.sample(code_range, 12))
    date = datetime.datetime.now()
    bot_info = await bot.get_me()
    user_tg_ig = callback.from_user.id
    await DataBase.add_code(permission_code=str(permission_code), name=name, creater_tg_id=user_tg_ig, created_at=date)
    await callback.message.edit_text(f"Код с названием {name} успешно создан\n<code>{f"https://t.me/{bot_info.username}?start={permission_code}"}</code>")
    await callback.answer()


@router_create_code.callback_query(F.data == "cancel_create_code")
async def cancel_create_code(callback: types.CallbackQuery):
    await callback.message.edit_text(f"Создание кода отменено")
    await callback.answer()