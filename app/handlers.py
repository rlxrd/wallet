from aiogram import types, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.database.requests import *
import app.keyboards as kb

router = Router()


class Registration(StatesGroup):
    name = State()
    currency = State()
    amount = State()


@router.message(Command('start'))
async def start_cmd(message: types.Message, state: FSMContext):
    user_reg = await add_user_db(message.from_user.first_name, message.from_user.id)
    if not user_reg:
        await state.set_state(Registration.name)
        await message.answer('Добро пожаловать в бот Pro Waller!\n\nНаша задача - помочь Вам с учётом личных финансов. Здесь вы можете контролировать свои расходы и доходы, а также их анализировать! Давайте создадим Ваш первый счёт для начала работы с ботом.\n\nВведите название счёта.')
    else:
        await message.answer(f'Доброго времени суток, {message.from_user.first_name}!\n\nУправляйте счетами по кнопкам ниже.')


@router.message(Registration.name)
async def registration_name(message: types.Message, state: FSMContext):
    if len(message.text) > 35:
        await message.answer('Название слишком длинное! Максимум 32 символа.')
        return
    else:
        await state.update_data(name=message.text)
        await state.set_state(Registration.currency)
        await message.answer(f'Отличное название!\n\nВыберите, в какой валюте будет счёт {message.text}?', reply_markup=kb.all_currencies_kb())


@router.callback_query(Registration.currency)
async def registration_currency(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(currency=callback.data)
    await state.set_state(Registration.amount)
    await callback.answer(f'Выбрано.')
    await callback.message.answer('Теперь введите первоначальный баланс.\n\nДопускаются только целые числа, например: 50000')


@router.message(Registration.amount)
async def registration_amount(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            await state.update_data(amount=message.text)
            await state.update_data(user=message.from_user.id)
            reg_data = await state.get_data()
            reg_result = set_account_db(reg_data)
            if reg_result:
                await message.answer('Регистрация успешно завершена!')
            else:
                await message.answer('Произошла ошибка... Обратитесь к администратору @rlxrd')
    except:
        await message.answer('Ошибка!\n\nПопробуйте ввести целое число, без точек и запятых. Например, просто 123000')
