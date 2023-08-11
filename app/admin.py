from aiogram import types, Router, Bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from app.database.requests import add_currency_db
import app.keyboards as kb
import time
import asyncio
from aiogram.filters import Command, Filter
from config import ADMINS

admin = Router()


class AddCurrency(StatesGroup):
    name = State()
    code = State()


class AdminProtect(Filter):
    """
    Фильтр для проверки пользователя на админа
    """
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: types.Message):
        return message.from_user.id in self.admins


@admin.message(AdminProtect(), Command('apanel'))
async def apanel(message: types.Message):
    await message.answer('Админ-команды:\n\n/add_direction - добавление валюты')


@admin.message(AdminProtect(), Command('add_currency'))
async def add_currency(message: types.Message, state: FSMContext):
    await state.set_state(AddCurrency.name)
    await message.answer('Введите название')


@admin.message(AdminProtect(), AddCurrency.name)
async def add_currency(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddCurrency.code)
    await message.answer('Введите код')


@admin.message(AdminProtect(), AddCurrency.code)
async def add_currency(message: types.Message, state: FSMContext):
    await state.update_data(code=message.text)
    data = await state.get_data()
    await add_currency_db(data)
    await state.clear()
    await message.answer('Выполнено.')

@admin.message()
async def unknown(message: types.Message):
    await message.delete()
