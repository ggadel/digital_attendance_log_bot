from aiogram import types

    
def create_code_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="Создать код", callback_data="create_code"),
            types.InlineKeyboardButton(text="Отмена", callback_data="cancel_create_code")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard