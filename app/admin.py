from aiogram import types, Router, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.database.requests import add_direction_db
import app.keyboards as kb
import time
import asyncio
from aiogram.filters import Command, Filter
from config import ADMINS

admin = Router()


class AddDirection(StatesGroup):
    name = State()


class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: types.Message):
        return message.from_user.id in self.admins


@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: types.Message):
    await message.answer('Админ-команды:\n\n/add_direction - добавление валюты')


@admin.message(AdminProtect(), Command('add_direction'))
async def add_direction(message: types.Message, state: FSMContext):
    await state.set_state(AddDirection.name)
    await message.answer('Введи название')


@admin.message(AdminProtect(), AddDirection.name)
async def add_direction_name(message: types.Message, state: FSMContext):
    add_direction_db(message.text)
    await message.answer('Готово')
    await state.clear()
