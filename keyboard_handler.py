from aiogram import Router, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging

router = Router()

# Создание клавиатуры с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Привет"),
            KeyboardButton(text="Пока")
        ]
    ],
    resize_keyboard=True
)

# Обработчик кнопки "Привет"
@router.message(F.text == "Привет")
async def handle_hello(message: Message):
    logging.info("Нажата кнопка Привет")
    await message.reply(f"Привет, {message.from_user.first_name}!")

# Обработчик кнопки "Пока"
@router.message(F.text == "Пока")
async def handle_goodbye(message: Message):
    logging.info("Нажата кнопка Пока")
    await message.reply(f"До свидания, {message.from_user.first_name}!")

# Команда /links для отображения инлайн-кнопок с URL-ссылками
@router.message(Command("links"))
async def send_links(message: Message):
    logging.info("Получена команда /links")
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://news.yandex.ru")],
        [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru")],
        [InlineKeyboardButton(text="Видео", url="https://youtube.com")]
    ])
    await message.reply("Выберите ссылку:", reply_markup=inline_keyboard)

# Команда /dynamic для отображения динамической инлайн-кнопки

@router.message(Command("dynamic"))
async def send_dynamic_menu(message: Message):
    logging.info("Получена команда /dynamic")

    # Создание инлайн-кнопки "Показать больше"
    builder = InlineKeyboardBuilder()
    builder.button(text="Показать больше", callback_data="show_more")
    keyboard = builder.as_markup()

    await message.reply("Выберите опцию:", reply_markup=keyboard)


# Обработчик для инлайн-кнопки "Показать больше"
@router.callback_query(F.data == "show_more")
async def show_more_options(callback_query: CallbackQuery):
    logging.info("Нажата кнопка Показать больше")

    # Создание новых инлайн-кнопок "Опция 1" и "Опция 2"
    builder = InlineKeyboardBuilder()
    builder.button(text="Опция 1", callback_data="option_1")
    builder.button(text="Опция 2", callback_data="option_2")
    keyboard = builder.as_markup()

    await callback_query.message.edit_text("Выберите опцию:", reply_markup=keyboard)


# Обработчик для инлайн-кнопок "Опция 1" и "Опция 2"
@router.callback_query(F.data.in_({"option_1", "option_2"}))
async def handle_option(callback_query: CallbackQuery):
    option = callback_query.data
    option_text = option.replace('option_1', 'Опция 1').replace('option_2', 'Опция 2')
    logging.info(f"Нажата кнопка {option_text}")

    await callback_query.message.answer(f"Вы выбрали {option_text}")
    await callback_query.answer()  # Закрыть всплывающее уведомление

