import asyncio

from io import BytesIO

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, BufferedInputFile

from markups import main_markup, my_orders_markup, edit_order_markup, view_order_markup
from states import RegForm, OrderForm, SelectOrder, EditOrder
from database import Database
from config import config

dp = Dispatcher()


@dp.message(Command("menu"))
async def menu(message: Message):
    await message.answer("Головне меню.", reply_markup=main_markup)  # Головне меню.


@dp.message(lambda msg: msg.text in ["Головне меню", "Hauptmenü."])
async def menu(message: Message):
    await message.answer("Головне меню.", reply_markup=main_markup)  # Головне меню.


class Register:
    @staticmethod
    @dp.message(CommandStart())  # Обробка повідомлення
    async def start(message: Message, state: FSMContext):  # Оголошення асинхронної функції, (параметри)
        await state.set_state(RegForm.name)  # Встановлення стану
        await message.answer("Вітаю! Введіть ваше ім'я.")

    @staticmethod
    @dp.message(RegForm.name)
    async def process_name(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(RegForm.surname)
        await message.answer("Введіть ваше прізвище")

    @staticmethod
    @dp.message(RegForm.surname)
    async def process_surname(message: Message, state: FSMContext):
        await state.update_data(surname=message.text)
        await state.set_state(RegForm.phone)
        await message.answer("Введіть ваш телефон.")

    @staticmethod
    @dp.message(RegForm.phone)
    async def process_phone(message: Message, state: FSMContext):
        data = await state.update_data(phone=message.text)
        await state.clear()

        Database.register_user(data)

        await message.answer(f"✅ Реєстрація завершена", reply_markup=main_markup)


class CreateOrder:
    @staticmethod
    @dp.message(lambda msg: msg.text == "Створити оголошення.")  # Створити оголошення.
    async def process_order(message: Message, state: FSMContext):
        await state.set_state(OrderForm.brand)
        await message.answer(" Введіть марку автомобіля.")  # Введіть марку автомобіля.

    @staticmethod
    @dp.message(OrderForm.brand)
    async def process_brand(message: Message, state: FSMContext):
        await state.update_data(brand=message.text)
        await state.set_state(OrderForm.model)
        await message.answer("Введіть модель.")  # Введіть модель.

    @staticmethod
    @dp.message(OrderForm.model)
    async def process_model(message: Message, state: FSMContext):
        await state.update_data(model=message.text)
        await state.set_state(OrderForm.description)
        await message.answer("Введіть опис.")  # Введіть опис.

    @staticmethod
    @dp.message(OrderForm.description)
    async def process_description(message: Message, state: FSMContext):
        await state.update_data(description=message.text)
        await state.set_state(OrderForm.price)
        await message.answer("Введіть ціну")  # Введіть ціну.

    @staticmethod
    @dp.message(OrderForm.price)
    async def process_price(message: Message, state: FSMContext):
        await state.update_data(price=message.text)
        await state.set_state(OrderForm.photo)
        await message.answer("Надішліть фото автомобіля.")  # Надішліть фото автомобіля.

    @staticmethod
    @dp.message(OrderForm.photo)
    async def process_photo(message: Message, state: FSMContext):
        image = BytesIO()
        await message.bot.download(file=message.photo[-1].file_id, destination=image)

        data = await state.update_data(photo=image.read())
        await state.clear()

        Database.create_order(user_id=message.from_user.id, data=data)

        await message.answer("✅ Оголошення створено.")  # Оголошення створено.


class ViewOrders:
    @staticmethod
    @dp.message(lambda msg: msg.text == "Bestellungen ansehen.")  # Переглянути замовлення.
    async def view_orders(message: Message):
        await message.answer("Liste der Bestellungen.", reply_markup=view_order_markup)  # Список замовлень

    @staticmethod
    @dp.message(lambda msg: msg.text == "Hauptmenü.")  # Головне меню.
    async def main_menu(message: Message):
        await message.answer("Hauptmenü.", reply_markup=main_markup)  # Головне меню.


class MyOrders:
    @staticmethod
    @dp.message(lambda msg: msg.text in ["Мої оголошення", ""])
    async def show_orders(message: Message, state: FSMContext):
        orders = Database.get_orders(user_id=message.from_user.id)

        text = "*Список оголошень*\n\n"

        for i, order in enumerate(orders, 1):  
            text += f"`{i}`. {order[2]} {order[3]}\n"

        # TODO: Ви не маєте жодного оголошення
        text += "\nВведіть номер оголошення яке хочете редагувати"

        await state.set_state(SelectOrder.order_index)
        await message.answer(text, parse_mode="Markdown", reply_markup=my_orders_markup)

    @staticmethod
    @dp.message(SelectOrder.order_index)
    async def show_order(message: Message, state: FSMContext):
        data = await state.update_data(order_index=message.text)
        await state.clear()

        orders = Database.get_orders(user_id=message.from_user.id)

        if not data["order_index"].isnumeric():
            await message.answer("ВВЕДИ ЧИСЛО")
            await state.set_state(SelectOrder.order_index)
            return

        order_index = int(data["order_index"]) - 1

        if not -1 < order_index < len(orders):
            await message.answer("Не вірний номер оголошення")
            await state.set_state(SelectOrder.order_index)
            return

        int("12")
        str(SelectOrder)

        order = orders[order_index]

        print(order)
        await message.answer(str(order))  # TODO: Редагування оголошення


async def main():
    bot = Bot(token=config["token"])
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
