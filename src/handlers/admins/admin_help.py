import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command




router_admin_help = Router()


@router_admin_help.message(F.text, Command("admin_help", "админ_помощь"))
async def admin_help(message: Message):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    await message.answer("<b>Список админ команд:</b>\n\n/get_absent [DD-MM-YYYY] - получить список отсутствующих в определнную дату(в аргументах указать дату в формате DD-MM-YYYY)\n\n/remove_entry [айди записи] - удалить запись из журнала\n\n/add_class [класс] или /add_class [класс1, класс2] - добавить класс в список доступных для выбора\n\n/remove_class [класс] или /remove_class [класс1, класс2] - удалить класс\n\n/list_of_classes - список классов\n\n/get_user [айди пользователя] - получить информацию о пользователе\n\n/ban [user_tg_id] - заблокировать пользователя\n\n/unban [user_tg_id] - разблокировать пользователя\n\n/create_code [название кода] - создать ссылку приглашение\n\n/remove_code [id] - удалить ссылку приглашение\n\n/get_codes - получить список ссылок приглашений\n\n/give_permission [user_tg_id] - выдать разрешение отмечать отсутствующих\n\n/remove_permission [user_tg_id] - забрать разрешение отмечать отсутствующих\n\n/admin_panel или /панель - админ панель")