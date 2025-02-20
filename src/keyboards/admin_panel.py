from aiogram import types

    
def admin_panel_kb():
    buttons = [
        [
            types.InlineKeyboardButton(text="Получить отсутствующих по классам", callback_data="get_absent")
        ],
        [
            types.InlineKeyboardButton(text="Получить всех отсутствующих", callback_data="get_absent_all")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard