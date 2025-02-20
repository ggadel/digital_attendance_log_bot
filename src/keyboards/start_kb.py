from aiogram import types

    
def start_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton('Команда 1'))
    kb.add(types.KeyboardButton('Команда 2'))
    kb.row(types.KeyboardButton('Команда 3'), types.KeyboardButton('Команда 4'))
    return kb