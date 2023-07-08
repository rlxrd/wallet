from aiogram import types, Router
from aiogram.filters import Command
from app.database.requests import *

router = Router()


@router.message(Command('start'))
async def start_cmd(message: types.Message):
    await add_user_db(message.from_user.first_name, message.from_user.id)
    await message.answer('Добро пожаловать!')
