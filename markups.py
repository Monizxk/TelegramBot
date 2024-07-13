from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


main_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Створити оголошення."),  # Створити оголошення.
        KeyboardButton(text="Переглянути оголошення."),  # Переглянути оголошення.
        KeyboardButton(text="Мої оголошення"),
    ]
], resize_keyboard=True)


view_order_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Головне меню."),  # Головне меню.
        KeyboardButton(text="Далі.")  # Далі.
    ]
], resize_keyboard=True)


my_orders_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Головне меню")
    ]
], resize_keyboard=True)


edit_order_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Редагувати бренд"),
        KeyboardButton(text="Редагувати модель"),
        KeyboardButton(text="Редагувати опис")
    ],
    [
        KeyboardButton(text="Редагувати ціну"),
        KeyboardButton(text="Редагувати фото"),
        KeyboardButton(text="Видалити :з")
    ]
], resize_keyboard=True)
