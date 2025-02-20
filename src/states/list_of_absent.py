from aiogram.fsm.state import State, StatesGroup


class List_of_absent(StatesGroup):
    class_name = State()
    amount_class = State() 
    amount_absent = State() 
    list_of_absent = State()
    last_used = State()