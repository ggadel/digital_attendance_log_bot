import logging
import datetime
import json
from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.database.queries import DataBase

from src.keyboards.cancel_form_kb import cancel_form
from src.keyboards.admin_panel import admin_panel_kb

from src.states.get_absent import Get_absent
from src.data.config import PATH_TO_LIST_OF_CLASSES

router_admin_panel = Router()


@router_admin_panel.message(F.text, Command("admin_panel", "панель"))
async def start(message: Message):
    logging.info(f"Пользователь {message.from_user.id} использовал команду {message.text}")
    await message.answer("Админ панель: \n\nполучить список отсутствующих", reply_markup=admin_panel_kb())



@router_admin_panel.callback_query(F.data == "get_absent" or F.data == "get_absent_all")
async def get_absent(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f"Пользователь {callback.from_user.id} использовал команду {callback.data}")
    await state.update_data(func_type = callback.data)
    await state.set_state(Get_absent.date)
    await callback.message.answer("Введите дату в формате: <code>[DD-MM-YYYY]</code>", reply_markup=cancel_form())
    await callback.answer()


@router_admin_panel.callback_query(F.data == "get_absent_all")
async def get_absent_all(callback: types.CallbackQuery, state: FSMContext):
    logging.info(f"Пользователь {callback.from_user.id} использовал команду {callback.data}")
    await state.update_data(func_type = callback.data)
    await state.set_state(Get_absent.date)
    await callback.message.answer("Введите дату в формате: <code>[DD-MM-YYYY]</code>", reply_markup=cancel_form())
    await callback.answer()


@router_admin_panel.callback_query(F.data == "cancel_form")
async def button_cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    
    current_state = await state.get_state()
    if current_state is None:
        await callback.answer()
        return
    await state.clear()
    await callback.message.answer("Заполнение формы отменено.")  
    await callback.answer()


async def cancel_handler(message: Message, state: FSMContext, error_text):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(f"Заполнение формы отменено. {error_text}")


@router_admin_panel.message(Get_absent.date)
async def get_absent_func(message: Message, state: FSMContext):
    date = message.text
    data = await state.get_data()
    if data["func_type"] == "get_absent":
        try:
            date_format = "%d-%m-%Y"
            formatted_date = datetime.datetime.strptime(date, date_format)
            result = await DataBase.get_absent(date=formatted_date)
            if len(result) == 0:
                await message.answer("В этот день записи отсутствуют")
                return
            formatted_msg = []
            with open(PATH_TO_LIST_OF_CLASSES, 'r') as f:
                list_of_classes = json.load(f)
                len_list = 0
                
                await message.answer(f"Отмеченные классы за {formatted_date}:\n\nСписок не отмеченных классов: {", ".join(list_of_classes)}")
                
                for row in result:
                    formatted_str = f"<pre> id записи: {row[0]}\n Класс: {row[1]}\n Учащихся: {row[2]}\n Отсутствует: {row[3]}\n отсутствующие: {row[4]}\n Добавил: {row[5]}, @{row[6]}\n Время: {str(row[8]).split('.')[0]}</pre>"
                    
                    if row[1] in list_of_classes:
                        list_of_classes.remove(row[1])
                    formatted_msg.append(formatted_str)
                    
                    if len_list >= 10:
                        len_list = 0
                        await message.answer(f"{"\n".join(formatted_msg)}")
                        formatted_msg = []
                    len_list += 1
                if len(formatted_msg) != 0:
                    await message.answer(f"{"\n".join(formatted_msg)}")
                await state.clear()
        except:
            await message.answer("Ошибка: Неверно переданы аргменты. Введите дату  в формате: <code>[DD-MM-YYYY]</code>")
            await state.clear()
    elif data["func_type"] == "get_absent_all":
        try:
            date_format = "%d-%m-%Y"
            formatted_date = datetime.datetime.strptime(date, date_format)
            result = await DataBase.get_absent(date=formatted_date)
            if len(result) == 0:
                await message.answer("В этот день записи отсутствуют")
                return
            formatted_msg = []
            amount_of_absent = 0
            for row in result:
                formatted_str = f"{row[1]}:  {row[4]}"
                formatted_msg.append(formatted_str)
                amount_of_absent += row[3]
            await message.answer(f"Список и количесто всех отсутствующих за {formatted_date}:\n\nВсего отстутствует: {str(amount_of_absent)}\nСписок отсутствующих: \n{"\n".join(formatted_msg)}")
            await state.clear()
        except:
            await message.answer("Ошибка: Неверно переданы аргменты. Введите дату  в формате: <code>[DD-MM-YYYY]</code>")
            await state.clear()