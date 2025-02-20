from aiogram.fsm.state import State, StatesGroup


class Get_absent(StatesGroup):
    func_type = State()
    date = State()