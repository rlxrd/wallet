from aiogram import types, Router
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.database.requests import *
import app.keyboards as kb
import time
import asyncio
from aiogram import Bot

router = Router()


# Состояния
class Registration(StatesGroup):
    name = State()
    currency = State()
    amount = State()


class TopUp(StatesGroup):
    amount = State()
    account = State()
    direction = State()
    

# Главный обработчик + проверка на созданный счет
@router.message(Command('start'))
async def start_cmd(message: types.Message, state: FSMContext):
    start_time = time.time()
    user_reg = await add_user_db(message.from_user.first_name, message.from_user.id)
    if not user_reg:
        await state.set_state(Registration.name)
        await message.answer('Добро пожаловать в бот Pro Wallet!\n\nНаша задача - помочь Вам с учётом личных финансов. Здесь вы можете контролировать свои расходы и доходы, а также их анализировать! Давайте создадим Ваш первый счёт для начала работы с ботом.\n\nВведите название счёта.', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f'Доброго времени суток, {message.from_user.first_name}!\n\nУправляйте счетами по кнопкам ниже.', reply_markup=kb.main_kb)
    end_time = time.time()
    await message.answer(f'Время выполнения: {end_time - start_time}')


# Регистрация счета
@router.message(Registration.name)
async def registration_name(message: types.Message, state: FSMContext, bot: Bot):
    start_time = time.time()
    if len(message.text) > 35:
        await message.answer('Название слишком длинное! Максимум 32 символа.')
        return
    else:
        await state.update_data(name=message.text)
        await state.set_state(Registration.currency)
        await message.answer(f'Отличное название!\n\nВыберите, в какой валюте будет счёт {message.text}?', reply_markup=kb.all_currencies_kb())
    end_time = time.time()
    await message.answer(f'Время выполнения: {end_time - start_time}')


@router.callback_query(Registration.currency)
async def registration_currency(callback: types.CallbackQuery, state: FSMContext):
    start_time = time.time()
    if check_currency_db(callback.data):
        await state.update_data(currency=callback.data)
        await state.set_state(Registration.amount)
        await callback.answer(f'Выбрано.')
        await callback.message.answer('Теперь введите первоначальный баланс.\n\nДопускаются только целые числа, например: 50000')
    else:
        await callback.message.answer('Ошибка... Такой валюты нету.')
    end_time = time.time()
    await callback.message.answer(f'Время выполнения: {end_time - start_time}')


@router.message(Registration.amount)
async def registration_amount(message: types.Message, state: FSMContext):
    start_time = time.time()
    if message.text.isdigit():
        await state.update_data(amount=message.text)
        await state.update_data(user=message.from_user.id)
        reg_data = await state.get_data()
        if set_account_db(reg_data):
            await message.answer(f'Регистрация успешно завершена!\n\nТеперь Вы можете управлять своими счетами по кнопкам ниже.', reply_markup=kb.main_kb)
            await state.clear()
        else:
            await message.answer('Произошла ошибка... Обратитесь к администратору @rlxrd', reply_markup=kb.main_kb)
            await state.clear()
    else:
            await message.answer('Упс... Вводить сумму нужно целым числом, например 123000.')
    end_time = time.time()
    await message.answer(f'Время выполнения: {end_time - start_time}')


# Пополнение баланса
@router.callback_query(lambda c: c.data == 'topup')
async def topup(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Введите сумму')
    await state.set_state(TopUp.amount)
    await callback.message.edit_text('Вы хотите <b>пополнить</b> баланс. Введите сумму в виде целого числа.')


@router.message(TopUp.amount)
async def topup_amount(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(amount=message.text)
        await state.set_state(TopUp.account)
        await message.answer('Выберите счёт для пополнения', reply_markup=kb.top_up_kb(message.from_user.id))
    else:
        await message.answer('Отправьте целое число, например 123000')


@router.callback_query(TopUp.account)
async def topup_account(callback: types.CallbackQuery, state: FSMContext):
    if fetch_account_db(callback.data):
        await callback.answer('Записали...')
        await state.update_data(account=callback.data)
        await state.set_state(TopUp.direction)
        await callback.message.answer('Теперь выберите направление!', reply_markup=kb.directions_topup_kb())
    else:
        await callback.answer('Ошибка')
    

@router.callback_query(TopUp.direction)
async def topup_direction(callback: types.CallbackQuery, state: FSMContext):
    if fetch_directions_check(callback.data):
        await callback.answer('Записали...')
        await state.update_data(direction=callback.data)
        data = await state.get_data()
        update_balance_db(data)
        await callback.message.answer('Готово!', reply_markup=kb.main_kb)
    else:
        await callback.answer('Ошибка')
