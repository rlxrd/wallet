from aiogram import types, Router, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from app.database.requests import *
import app.keyboards as kb
import asyncio

router = Router()


# Состояния
class Registration(StatesGroup):
    name = State()
    currency = State()
    amount = State()
    sure = State()


class TopUp(StatesGroup):
    account = State()
    amount = State()
    category = State()
    direction = State()
    sure = State()


class Spend(StatesGroup):
    account = State()
    amount = State()
    category = State()
    direction = State()
    sure = State()


class DeleteAcc(StatesGroup):
    sure = State()

"""

Главный обработчик + проверка на созданный счёт.

"""

# Главный обработчик + проверка на созданный счет
@router.message(Command('start'))
async def start_cmd(message: types.Message, state: FSMContext):
    user_reg = await add_user_db(message.from_user.id)
    if not user_reg:
        await state.set_state(Registration.name)
        await message.answer('👋 Добро пожаловать в бот Pro Wallet!\n\nНаша задача - помочь Вам с учётом личных финансов. Здесь вы можете контролировать свои расходы и доходы, а также их анализировать! Давайте создадим Ваш первый счёт для начала работы с ботом.\n\n👉 Введите название счёта. Например: Основной.',
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f'💸 Доброго времени суток, {message.from_user.first_name}!\n\nУправляйте счетами по кнопкам ниже. 👇', reply_markup= kb.main_kb)


# Отмена действий
@router.callback_query(F.data == 'cancel')
async def cancel(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        print('error 1')
    try:
        await state.clear()
    except:
        print('error 2')
    await callback.message.answer(f'💸 Доброго времени суток, {callback.from_user.first_name}!\n\nУправляйте счетами по кнопкам ниже. 👇', reply_markup=kb.main_kb)


"""

Регистрация счёта!

"""

@router.message(Registration.name)
async def registration_name(message: types.Message, state: FSMContext):
    if len(message.text) > 18:
        await message.answer('❌ Название слишком длинное! Максимум 18 символа.')
        return
    else:
        await state.update_data(name=message.text)
        await state.set_state(Registration.currency)
        await message.answer(f'✅ Отличное название!\n\nВыберите, в какой валюте будет счёт {message.text}? 👇', reply_markup=await kb.all_currencies_kb())


@router.callback_query(Registration.currency)
async def registration_currency(callback: types.CallbackQuery, state: FSMContext):
    if not await check_currency_db(callback.data):
        await callback.message.answer('❌ Ошибка... Такой валюты нету.')
    else:
        await state.update_data(currency=callback.data)
        await state.set_state(Registration.amount)
        await callback.answer(f'Выбрано.')
        await callback.message.edit_text('✅ Теперь введите первоначальный баланс.\n\nНапример: 12.500 👇')


@router.message(Registration.amount)
async def registration_amount(message: types.Message, state: FSMContext):
    try:
        if 0 <= float(message.text) <= 9999999999999:
            await state.update_data(amount=float(message.text))
            await state.update_data(user=message.from_user.id)
            reg_data = await state.get_data()
            currency = await check_currency_db(reg_data["currency"])
            await state.set_state(Registration.sure)
            await message.answer(f'🔒 Информация о счёте:\n\nНазвание: {reg_data["name"]}\nБаланс: {reg_data["amount"]} {currency.name}\n\nПроверьте и подтвердите 👇', reply_markup=kb.sure)
        else:
            await message.answer('❌ Введите корректное число.')
    except Exception as error:
        await message.answer(f'❌ Пожалуйста введите число, например: 13.200, {error}')    
            

@router.callback_query(F.data == 'yesyes', Registration.sure)
async def registration_done(callback: types.CallbackQuery, state: FSMContext):
    reg_data = await state.get_data()
    if await set_account_db(reg_data):
        await callback.message.edit_text(f'✅ Регистрация успешно завершена!\n\nТеперь Вы можете управлять своими счетами по кнопкам ниже.', reply_markup=kb.main_kb)
        await state.clear()
    else:
        await callback.message.answer('❌ Произошла ошибка... Обратитесь к администратору @rlxrd', reply_markup=kb.main_kb)
        await state.clear()


@router.callback_query(F.data == 'nono', Registration.sure)
async def registration_canceled(callback: types.CallbackQuery, state: FSMContext):
    user_reg = await add_user_db(callback.from_user.id)
    if not user_reg:
        await state.set_state(Registration.name)
        await callback.message.answer('🤔 Введите название счёта. Например: Основной.', reply_markup=ReplyKeyboardRemove())
    else:
        await callback.message.answer(f'💸 Доброго времени суток, {callback.from_user.first_name}!\n\nУправляйте счетами по кнопкам ниже. 👇', reply_markup= kb.main_kb)


"""

Пополнение баланса!

счет
сумма
категория
направление
подтверждение
"""


@router.callback_query(F.data == 'topup')
async def topup(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(TopUp.account)
    await callback.answer('Вы выбрали пополнение.')
    try:
        await callback.message.delete()
    except Exception as err:
        print(err)
    await callback.message.answer('🔒 Выберите счёт для <b>пополнения</b>.', reply_markup=await kb.users_accounts_kb(callback.from_user.id))


@router.callback_query(TopUp.account)
async def topup_account(callback: types.CallbackQuery, state: FSMContext):
    acc_data = await check_account_db(callback.data)
    if not acc_data:
        await callback.message.answer('❌ Выбранного счета не существует!')
    else:
        try:
            currency_info = await check_currency_db(acc_data.currency)
            await state.update_data(account=callback.data)
            await state.set_state(TopUp.amount)
            await callback.answer(f'Вы выбрали {acc_data.name}')
            await callback.message.edit_text(f'🔒 Вы выбрали счёт {acc_data.name}.\n\nВведите, на сколько {currency_info.name} вы хотите его пополнить. 👇')
        except:
            await callback.message.edit_text(f'Выбранного счета не существует.')


@router.message(TopUp.amount)
async def topup_amount(message: types.Message, state: FSMContext):
    try:
        if float(message.text) < 9999999999999:
            await state.update_data(amount=float(message.text))
            await state.set_state(TopUp.category)
            await message.answer('🎯 Теперь выберите направление.', reply_markup= await kb.categiroes_kb(True))
        else:
            await message.answer('❌ Число слишком большое!')
    except:
        await message.answer('❌ Пожалуйста, введите число. Например: 17.145')


@router.callback_query(TopUp.category)
async def topup_category(callback: types.CallbackQuery, state: FSMContext):
    category_check = await check_categories(callback.data)
    if not category_check:
        await callback.message.answer('❌ Такой категории нет!')
    else:
        await state.set_state(TopUp.direction)
        await callback.message.edit_text(f'Выберите направление.', reply_markup= await kb.directions_kb(callback.data))


@router.callback_query(TopUp.direction)
async def topup_directions(callback: types.CallbackQuery, state: FSMContext):
    direct_check = await get_directions(callback.data)
    if not direct_check:
        await callback.message.answer('❌ Такого направления нет!')
    else:
        await state.update_data(direction=callback.data)
        await state.set_state(TopUp.sure)
        tdata = await state.get_data()
        await update_balance(tdata["amount"], tdata["account"], tdata["direction"], True)
        await callback.message.edit_text(f'✅ Счёт успешно пополнен!\n\nУправляйте счетами по кнопкам ниже. 👇', reply_markup= kb.main_kb)
        await state.clear()

"""

Смотреть свои счета

"""

@router.callback_query(F.data == 'myaccounts')
async def my_accounts(callback: types.CallbackQuery):
    await callback.answer('')
    try:
        await callback.message.delete()
    except Exception as err:
        print(err)
    await callback.message.answer('Ваши счета 👇', reply_markup= await kb.my_accs(callback.from_user.id))


@router.callback_query(F.data.startswith('acc_'))
async def edit_my_acc(callback: types.CallbackQuery):
    acc_id = callback.data.split('_')[1]
    account = await check_account_db(acc_id)
    try:
        cur = await check_currency_db(account.currency)
        await callback.message.edit_text(f'Вы выбрали счёт: {account.name}\nБаланс: {account.balance} {cur.name}\nID: {account.id}', reply_markup= await kb.acc_settings(acc_id))
    except:
        await callback.message.edit_text(f'Выбранный счет отсутствует.')
        await asyncio.sleep(3)
        await callback.message.edit_text('Ваши счета 👇', reply_markup= await kb.my_accs(callback.from_user.id))


# Удаление счета
@router.callback_query(F.data.startswith('delete_'))
async def delete_my_acc(callback: types.CallbackQuery, state: FSMContext):
    acc_id = callback.data.split('_')[1]
    account = await check_account_db(acc_id)
    cur = await check_currency_db(account.currency)
    await state.set_state(DeleteAcc.sure)
    await state.update_data(account=acc_id)
    await callback.message.edit_text(f'Вы уверены, что хотите удалить счёт? {account.name}', reply_markup=kb.sure)


@router.callback_query(F.data == 'yesyes', DeleteAcc.sure)
async def edit_my_acc(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await delete_acc(data)
    await callback.message.edit_text('Счёт успешно удален.')
    await state.clear()
    await asyncio.sleep(1.5)
    await callback.message.edit_text('Ваши счета 👇', reply_markup= await kb.my_accs(callback.from_user.id))


@router.callback_query(F.data == 'nono', DeleteAcc.sure)
async def edit_my_acc(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        print('error 1')
    try:
        await state.clear()
    except:
        print('error 2')
    await callback.message.answer(f'💸 Доброго времени суток, {callback.from_user.first_name}!\n\nУправляйте счетами по кнопкам ниже. 👇', reply_markup=kb.main_kb)


"""

ПОТРАТИТЬ

"""

@router.callback_query(F.data == 'spend')
async def spend(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Spend.account)
    await callback.answer('Вы выбрали расход.')
    try:
        await callback.message.delete()
    except Exception as err:
        print(err)
    await callback.message.answer('🔒 Выберите счёт для <b>расхода</b>.', reply_markup= await kb.users_accounts_kb(callback.from_user.id))


@router.callback_query(Spend.account)
async def spend_account(callback: types.CallbackQuery, state: FSMContext):
    acc_data = await check_account_db(callback.data)
    if not acc_data:
        await callback.message.answer('❌ Выбранного счета не существует!')
    else:
        currency_info = await check_currency_db(acc_data.currency)
        await state.update_data(account=callback.data)
        await state.set_state(Spend.amount)
        await callback.answer(f'Вы выбрали {acc_data.name}')
        await callback.message.edit_text(f'🔒 Вы выбрали счёт {acc_data.name}.\n\nВведите, сумму расхода в {currency_info.name}. 👇')


@router.message(Spend.amount)
async def spend_amount(message: types.Message, state: FSMContext):
    try:
        if float(message.text) < 9999999999999:
            await state.update_data(amount=float(message.text))
            await state.set_state(Spend.category)
            await message.answer('🎯 Теперь выберите направление.', reply_markup= await kb.categiroes_kb(False))
        else:
            await message.answer('❌ Число слишком большое!')
    except:
        await message.answer('❌ Пожалуйста, введите число. Например: 11.100')


@router.callback_query(Spend.category)
async def spend_category(callback: types.CallbackQuery, state: FSMContext):
    category_check = await check_categories(callback.data)
    if not category_check:
        await callback.message.answer('❌ Такой категории нет!')
    else:
        await state.set_state(Spend.direction)
        await callback.message.edit_text(f'Выберите направление.', reply_markup= await kb.directions_kb(callback.data))


@router.callback_query(Spend.direction)
async def spend_directions(callback: types.CallbackQuery, state: FSMContext):
    direct_check = await get_directions(callback.data)
    if not direct_check:
        await callback.message.answer('❌ Такого направления нет!')
    else:
        await state.update_data(direction=callback.data)
        await state.set_state(Spend.sure)
        tdata = await state.get_data()
        await update_balance(tdata["amount"], tdata["account"], tdata["direction"], False)
        await callback.message.edit_text(f'✅ Расход успешно записан!\n\nУправляйте счетами по кнопкам ниже. 👇', reply_markup= kb.main_kb)
        await state.clear()


"""

ПРОЧЕЕ

"""

@router.callback_query(F.data)
async def stats(callback: types.Message):
    await callback.answer('Данный раздел в разработке.')


@router.callback_query(F.data == 'last_trans')
async def last_stats(callback: types.Message):
    stats = await get_all_stats(callback.from_user.id)
    await callback.answer('Вы выбрали статистику.')
    try:
        await callback.message.delete()
    except Exception as err:
        print(err)
    await callback.message.answer('\n'.join(stats.values()), reply_markup=kb.back_ikb)
    

@router.callback_query(F.data == 'settings')
async def stats(callback: types.Message):
    await callback.answer('Данный раздел в разработке.')


@router.callback_query(F.data == 'premium')
async def stats(callback: types.Message):
    await callback.answer('Данный раздел в разработке.')
    

""" 

СОЗДАНИЕ НОВОГО СЧЕТА!

"""
@router.callback_query(F.data == 'add_new_acc')
async def add_new_acc(callback: types.Message, state: FSMContext):
    await state.set_state(Registration.name)
    await callback.message.answer(f'👉 Введите название счёта. Например: Основной.', reply_markup=kb.cancel_ikb)
