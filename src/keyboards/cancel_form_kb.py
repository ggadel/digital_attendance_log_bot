from aiogram import types

    
def cancel_form():
    buttons = [
        [
            types.InlineKeyboardButton(text="Отмена", callback_data="cancel_form")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard