import logging
import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.state import StateFilter

router = Router()

class VoiceState(StatesGroup):
    waiting_for_voice = State()

# Команда /voice
@router.message(Command("voice"))
async def send_voice_prompt(message: Message, state: FSMContext):
    logging.info("Получена команда /voice")
    await message.reply("Пожалуйста, запишите и отправьте голосовое сообщение.")
    await state.set_state(VoiceState.waiting_for_voice)

# Обработчик голосовых сообщений
@router.message(F.voice, StateFilter(VoiceState.waiting_for_voice))
async def handle_voice(message: Message, state: FSMContext):
    logging.info("Получено голосовое сообщение")
    file_info = await message.bot.get_file(message.voice.file_id)
    file_path = file_info.file_path
    file_name = os.path.join("voice", file_info.file_unique_id + ".ogg")
    os.makedirs("voice", exist_ok=True)
    await message.bot.download_file(file_path, file_name)
    await message.reply_voice(message.voice.file_id)
    await state.clear()
