import logging
import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, CommandObject

from src.database.queries import DataBase

from src.keyboards.mark_absent_kb import mark_absent_kb
from src.data.config import DEVLOPER_USER_NAME


router_start = Router()


@router_start.message(CommandStart(deep_link=True))
@router_start.message(F.text, Command("start"))
async def start_deep_link(message: Message, command: CommandObject):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    current_date = datetime.datetime.now()
    user_tg_id = message.from_user.id
    username = message.from_user.username
    check_user = await DataBase.check_user(user_tg_id=user_tg_id, current_username=username)
    if check_user == False:
        await DataBase.update_username(user_tg_id=user_tg_id, new_username=username)
    elif check_user == "User not found":
        await DataBase.add_user(user_tg_id=user_tg_id, username=username, registered_at=current_date)
    if command.args != None:
        permission_code = command.args
        code = await DataBase.check_permission_code(permission_code=permission_code)
        if code != False:
            await DataBase.give_mark_permission(user_tg_id=message.from_user.id, permission_code_id=code[0])
    await message.answer(f"<b>Электронный журнал посещаемости\n\nНикому не сообщайте адрес бота!</b>\n\nСписок всех комманд: /help\n\n\n<b>Чтобы отметить отсутствующих, нажмите на кнопку ниже и следуйте дальнейшим инструкциям</b>\n\n<i>*Разработано @{DEVLOPER_USER_NAME}</i>", reply_markup=mark_absent_kb())