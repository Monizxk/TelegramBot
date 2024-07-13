from aiogram.fsm.state import State, StatesGroup


class RegForm(StatesGroup):
    name = State()
    surname = State()
    phone = State()


class OrderForm(StatesGroup):
    brand = State()
    model = State()
    description = State()
    price = State()
    photo = State()


class SelectOrder(StatesGroup):
    order_index = State()


class EditOrder(StatesGroup):
    brand = State()
    model = State()
    description = State()
    price = State()
    photo = State()
