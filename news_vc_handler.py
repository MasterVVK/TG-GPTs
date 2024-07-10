# news_vc_handler.py

import requests
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("news_vc"))
async def send_vc_news(message: Message):
    url = 'https://api.vc.ru/v2/timeline?subsite_id=all'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        news = "\n\n".join([f"{item['title']} - {item['url']}" for item in data['result']['items'][:5]])
        await message.reply(news)
    else:
        await message.reply("Не удалось получить новости. Попробуйте позже.")
