import os
import asyncio
import logging
from config import TOKEN

from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import db_main


async def main():
    
    bot = Bot(token=TOKEN, parse_mode='HTML')
    await db_main()
    dp = Dispatcher()
    dp.include_router(router)
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
