import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

import aiohttp
import whisper  # может быть изменён на faster-whisp

API_TOKEN = ""

# Инициализация
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Параметры для Whisper :"base", "small", "medium", "large"
model = whisper.load_model("small")


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Отправь мне голосовое или видеосообщение, и я переведу его в текст!")


@dp.message(F.content_type == ContentType.TEXT)
async def ignore_text(message: Message):
    # Просто игнорируем текст
    pass


async def download_file(file_id: str, filename: str) -> str:
    # скачиваем тг файл на диск
    file = await bot.get_file(file_id)
    file_path = file.file_path
    url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()
            with open(filename, "wb") as f:
                f.write(data)
    return filename


@dp.message(F.voice)
async def voice_handler(message: Message):
    file_id = message.voice.file_id
    filename = f"voice_{message.voice.file_unique_id}.ogg"
    path = await download_file(file_id, filename)

    result = model.transcribe(path, fp16=False)
    text = result["text"].strip()

    await message.answer(f"Расшифровка: {text}")
    os.remove(path)


@dp.message(F.video_note)
async def video_note_handler(message: Message):
    file_id = message.video_note.file_id
    filename = f"video_{message.video_note.file_unique_id}.mp4"
    path = await download_file(file_id, filename)

    result = model.transcribe(path, fp16=False)
    text = result["text"].strip()

    await message.answer(f"Расшифровка: {text}")
    os.remove(path)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
