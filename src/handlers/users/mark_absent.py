import logging
import datetime
import json
import time
from typing import Any, Dict

from aiogram import Router, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.data.config import PATH_TO_LIST_OF_CLASSES, ADMINS, MARK_ABSENT_CMD_DELAY

from src.keyboards.cancel_form_kb import cancel_form
from src.keyboards.check_data_kb import check_data_kb

from src.database.queries import DataBase

from src.states.list_of_absent import *




router_mark_absent = Router()




@router_mark_absent.callback_query(F.data == "mark_absent")
async def mark_absent(callback: types.CallbackQuery, state: FSMContext):
    user_tg_id = callback.from_user.id
    if await DataBase.check_mark_permission(user_tg_id=user_tg_id) == False:
        await callback.message.answer("У вас нет разрешения на заполнение формы")
        await callback.answer()
        return
    global current_date
    current_date = datetime.datetime.now()
    logging.info(f"Пользователь {callback.from_user.id} использовал команду {callback.data}")
    command_delay = MARK_ABSENT_CMD_DELAY #in second
    data = await state.get_data()
    if callback.from_user.id not in ADMINS:
        if 'last_used' in data:
            if time.time() - data['last_used'] < command_delay:
                minute = int(((command_delay - (time.time() - data['last_used'])) % 3600) / 60)
                second = int(((command_delay - (time.time() - data['last_used'])) % 3600) % 60)
                await callback.message.answer(f"До следующего использования осталось: {minute} минут {second} секунд")
                await callback.answer()
                return
    await state.set_state(List_of_absent.class_name)
    await callback.message.answer("Введите название класса: ", reply_markup=cancel_form())
    await callback.answer()


@router_mark_absent.message(List_of_absent.class_name)
async def get_class_name(message: Message, state: FSMContext):
    class_name = message.text
    with open(PATH_TO_LIST_OF_CLASSES, 'r') as f:
        class_list = json.load(f)
        if class_name.lower() not in class_list:
            error_text = "Класса не существует."
            await cancel_handler(message=message, state=state, error_text=error_text)
            return
        if await DataBase.check_form_completion(class_name=class_name, date=datetime.date.today()) == True:
            error_text = f"Класс '{class_name.lower()}' уже отмечен."
            await cancel_handler(message=message, state=state, error_text=error_text)
            return
        await state.update_data(class_name=class_name.lower())
        await state.set_state(List_of_absent.amount_class)
        await message.answer("Введите общее количество учащихся в классе: ", reply_markup=cancel_form())


@router_mark_absent.callback_query(F.data == "cancel_form")
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
    
    
@router_mark_absent.message(List_of_absent.amount_class)
async def get_amount_class(message: Message, state: FSMContext):
    try:
        int_msg = int(message.text)
        print(int_msg)
        if int_msg <= 0 or int_msg >= 100:
            error_text = "Значением может быть только целое число от '1' до '100'."
            await cancel_handler(message=message, state=state, error_text=error_text)
            return
        await state.update_data(amount_class = int_msg)
        await state.set_state(List_of_absent.amount_absent)
        await message.answer("Введите количество отсутствующих в классе: ", reply_markup=cancel_form())
    except:
        error_text = "Значением может быть только целое число."
        await cancel_handler(message=message, state=state, error_text=error_text)
    


@router_mark_absent.message(List_of_absent.amount_absent, F.text.casefold() == "0")
async def get_amount_absent_null(message: Message, state: FSMContext):
    int_msg = int(message.text)
    if int_msg == 0:
        await state.update_data(amount_absent = int_msg)
        await state.update_data(list_of_absent = None)
        global data
        data = await state.get_data()
        await state.set_state()
        await check_data(message=message, data=data, state=state)


@router_mark_absent.message(List_of_absent.amount_absent)
async def get_amount_absent(message: Message, state: FSMContext):
    try:
        int_msg = int(message.text)
        if int_msg <= 0 or int_msg >= 100:
            error_text = "Значением может быть только целое число от '0' до '100'."
            await cancel_handler(message=message, state=state, error_text=error_text)
            return
        await state.update_data(amount_absent = int_msg)
        await state.set_state(List_of_absent.list_of_absent)
        await message.answer("Введите \"фимилию\" и \"имя\" отсутствующих, через запятую\nПример: Иванов Иван, Петров Петр", reply_markup=cancel_form())
    except:
        error_text = "Значением может быть только целое число."
        await cancel_handler(message=message, state=state, error_text=error_text)
        


@router_mark_absent.message(List_of_absent.list_of_absent)
async def get_list_of_absent(message: Message, state: FSMContext):
    global data
    data = await state.get_data()
    split_msg = (message.text).split(",")
    if data['amount_absent'] != len(split_msg):
        error_text = "Количество людей в списке отличается от введенного выше количества отсутствующих."
        await cancel_handler(message=message, state=state, error_text=error_text)
        return
    for obj in split_msg:
        formatted_name = obj.title()
        final_name = []
        formatted_name = formatted_name.split(" ")
        for name in formatted_name:
            name = name.replace(" ", "")
            if name != "":
                final_name.append(name)
        if len(final_name) != 2:
            error_text = "Некорректный формат данных. Введите данные в правильном формате: \"фамилия\" и \"имя\"."
            await cancel_handler(message=message, state=state, error_text=error_text)
            return
    await state.update_data(list_of_absent=(message.text).split(","))
    data = await state.get_data()
    await check_data(message=message, data=data, state=state)
    await state.set_state()
    
    
async def check_data(message: Message, data: Dict[str, Any], state: FSMContext):
    if type(data['list_of_absent']) == list:
        global list_of_absent
        current_list = []
        for obj in data['list_of_absent']:
            formatted_name = obj.title()
            final_name = []
            formatted_name = formatted_name.split(" ")
            for name in formatted_name:
                name = name.replace(" ", "")
                if name != "":
                    final_name.append(name)
            current_list.append(" ".join(final_name))
        list_of_absent = ", ".join(current_list)
    else:
        list_of_absent = str(data['list_of_absent'])
    await message.answer(f"<b>Проверьте данные!</b>\n\nКласс: {data['class_name']}\nКоличество учащихся: {data['amount_class']}\nКоличество отсутствующих: {data['amount_absent']}\nСписок отсутствующих: {list_of_absent}", reply_markup=check_data_kb())
    
    
@router_mark_absent.callback_query(F.data == "send_form")
async def send_data(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    current_date = datetime.date.today()
    final_data = {
        'class_name': data["class_name"],
        'amount_of_students': data["amount_class"],
        'amount_of_absent': data["amount_absent"],
        'list_of_absent': list_of_absent,
        'date': current_date,
        'time': datetime.datetime.now().time(),
        'sender_tg_id': user_id
    }
    if await DataBase.check_form_completion(date=datetime.date.today(), class_name=data['class_name']) == True:
        await callback.answer(f"Ошибка. Класс '{data['class_name']}' уже отмечен.")
        return 
    await DataBase.send_form(final_data=final_data)
    logging.info(f"Пользователь {callback.from_user.id} отправил в базу данных данные: {final_data}")
    await callback.message.edit_reply_markup()
    await callback.message.edit_text(f"<b>Данные отправлены!</b>\n\nКласс: {data['class_name']}\nКоличество учащихся: {data['amount_class']}\nКоличество отсутствующих: {data['amount_absent']}\nСписок отсутствующих: {list_of_absent}")
    await state.update_data(last_used=time.time())
    await callback.answer()


@router_mark_absent.callback_query(F.data == "cancel_send_form")
async def cancel_send_data(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Заполнение формы отменено.", reply_markup=None)