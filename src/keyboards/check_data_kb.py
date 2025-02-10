from aiogram import types

    
def check_data_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="Отправить", callback_data="send_form"),
            types.InlineKeyboardButton(text="Отмена", callback_data="cancel_send_form")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard