import asyncio
import logging
from config import TOKEN

from app.database.models import async_main
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.admin import admin


# Основная функция для запуска бота
async def main():
    await async_main() # Запуск БД

    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_routers(router, admin) # Роутеры
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # Логгирование
    try:
        asyncio.run(main())
    except KeyboardInterrupt: # Слушаем Ctrl+C
        print('Exit')
