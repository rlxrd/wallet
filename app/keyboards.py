from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.database.requests import fetch_accounts_db, get_currencies_db, fetch_directions_topup


def all_currencies_kb():
    currencies = get_currencies_db()
    currencies_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=currency.name, callback_data=currency.id)] for currency in currencies])   
    return currencies_kb


main_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Пополнение', callback_data='topup'),
                                                 InlineKeyboardButton(text='Расход', callback_data='spend'),
                                                 InlineKeyboardButton(text='Мои счета', callback_data='myaccounts')],
                                                [InlineKeyboardButton(text='Статистика', callback_data='statistics'),
                                                 InlineKeyboardButton(text='Настройки', callback_data='settings'),
                                                 InlineKeyboardButton(text='Премиум', callback_data='premium')]])

def top_up_kb(tg_id):
    accounts = fetch_accounts_db(tg_id)
    accounts_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=acc.name, callback_data=acc.id)] for acc in accounts])
    return accounts_kb


def directions_topup_kb():
    directions = fetch_directions_topup()
    directions_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=direct.name, callback_data=direct.id)] for direct in directions])
    return directions_kb
