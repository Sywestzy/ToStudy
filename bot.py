import asyncio
import logging
import sys
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

load_dotenv()

# Получаем токен из переменной окружения
TOKEN = getenv("BOT_TOKEN")

# Проверяем наличие токена
if not TOKEN:
    print("Ошибка: не найден BOT_TOKEN в переменных окружения!")
    sys.exit(1)

# Создаем Dispatcher (корневой роутер)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start
    Этот обработчик срабатывает, когда пользователь отправляет команду /start
    """
    await message.answer(
        f"Привет, {html.bold(message.from_user.full_name)}!\n\n"
        f"Я твой первый бот на aiogram 3.22! 🚀"
    )

 
@dp.message(F.photo)
async def photo_handler(message: Message) -> None: 
    """
    Обработчик фото, возвращающий его с подписью в случае ее наличия
    или хуй в противном случае 
    """
    photo = message.photo[-1]
    caption = message.caption or "хуй"
    
    await message.answer_photo(
        photo = photo.file_id,
        caption = caption
    ) 
    
@dp.message(F.audio)
async def audio_handler(message: Message) -> None:
    audio = message.audio
    caption = message.caption 
    
    if not caption and (audio.performer or audio.title): 
        caption = f"{audio.performer or ''} - {audio.title or ''}".strip()
    elif not caption:
        caption = "penis"
    
    await message.answer_audio(
        audio = audio.file_id,
        caption = caption,
        performer = audio.performer,
        title = audio.title,
        duration = audio.duration
    )
    
@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Эхо-обработчик: отправляет копию полученного сообщения
    Этот обработчик срабатывает для всех остальных сообщений
    """
    # Проверяем, есть ли текст в сообщении
    if message.text:
        # Просто отправляем текст обратно
        await message.answer(message.text)
    
    else:
        # Если это не текстовое сообщение (фото, документ и т.д.)
        await message.answer("Попробуйте отправить текстовое сообщение!")
        
async def main() -> None:
    """
    Главная функция для запуска бота
    """
    # Инициализируем Bot с настройками по умолчанию
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Запускаем polling для получения обновлений
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Настраиваем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stdout
    )
    
    # Запускаем бота
    asyncio.run(main())