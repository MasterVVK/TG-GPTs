import logging
import os
from aiogram import Router, F
from aiogram.types import Message

router = Router()

# Папка для сохранения изображений
IMG_DIR = "img"
os.makedirs(IMG_DIR, exist_ok=True)

# Обработчик фотографий
@router.message(F.photo)
async def handle_photos(message: Message):
    logging.info("Получена фотография")
    for photo in message.photo:
        file_info = await message.bot.get_file(photo.file_id)
        file_path = file_info.file_path
        file_name = os.path.join(IMG_DIR, file_info.file_unique_id + ".jpg")
        await message.bot.download_file(file_path, file_name)
        await message.reply(f"Фото сохранено как {file_name}")
