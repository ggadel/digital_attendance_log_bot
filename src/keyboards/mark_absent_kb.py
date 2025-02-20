from aiogram import types

    
def mark_absent_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="Отметить отсутствующих", callback_data="mark_absent")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard