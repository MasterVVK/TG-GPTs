import logging
import json
import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from student_registration import router as student_router  # Импорт маршрутизатора
from keyboard_handler import router as keyboard_router, keyboard  # Импорт маршрутизатора для клавиатуры и кнопок
from weather_handler import router as weather_router  # Импорт маршрутизатора для погоды
from common_commands import router as common_router  # Импорт маршрутизатора для общих команд
from voice_handler import router as voice_router  # Импорт маршрутизатора для голосовых сообщений
from photo_handler import router as photo_router  # Импорт маршрутизатора для фотографий
from translator_handler import router as translator_router  # Импорт маршрутизатора для перевода
import aiohttp  # Импорт aiohttp для асинхронных запросов
from cat_api_handler import router as cat_router  # Импорт маршрутизатора для The Cat API
from nasa_api_handler import router as nasa_router  # Импорт маршрутизатора для NASA API
from news_vc_handler import router as news_vc_router  # Импорт маршрутизатора для новостей VC.ru
from random_recipe_handler import router as recipe_router  # Импорт маршрутизатора для случайных рецептов

# Загрузка конфигурации из файла config.json с явным указанием кодировки utf-8
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

API_TOKEN = config['API_TOKEN']
DEFAULT_CITY_NAME = config['DEFAULT_CITY_NAME']

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Установите уровень DEBUG для подробного логирования
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Создание объекта бота с кастомной сессией и настройками
session = AiohttpSession()
bot = Bot(
    token=API_TOKEN,
    session=session,
    default=DefaultBotProperties(parse_mode="HTML")
)

# Создание диспетчера и состояния
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(keyboard_router)  # Включение маршрутизатора для клавиатуры и кнопок
dp.include_router(student_router)  # Включение маршрутизатора
dp.include_router(weather_router)  # Включение маршрутизатора для погоды
dp.include_router(common_router)  # Включение маршрутизатора для общих команд
dp.include_router(voice_router)  # Включение маршрутизатора для голосовых сообщений
dp.include_router(photo_router)  # Включение маршрутизатора для фотографий
dp.include_router(cat_router)  # Включение маршрутизатора для The Cat API
dp.include_router(nasa_router)  # Включение маршрутизатора для NASA API
dp.include_router(news_vc_router)  # Включение маршрутизатора для новостей VC.ru
dp.include_router(recipe_router)  # Включение маршрутизатора для случайных рецептов
dp.include_router(translator_router)  # Включение маршрутизатора для перевода


# Команда /start с меню
@dp.message(Command("start"))
async def send_welcome(message: Message):
    logging.info("Получена команда /start")
    await message.reply("Привет! Я бот, созданный с помощью Aiogram. Используйте команду /weather &lt;город&gt; для получения прогноза погоды.", reply_markup=keyboard)

async def on_shutdown(bot: Bot):
    await bot.session.close()

async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(bot)

if __name__ == "__main__":
    asyncio.run(main())
