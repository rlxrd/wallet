from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.database.requests import *


def all_currencies_kb() -> InlineKeyboardMarkup:
    currencies = get_currencies_db()
    
    currencies_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=currency.name, callback_data=currency.id)] for currency in currencies])   
    return currencies_kb


main_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Пополнение', callback_data='topup'),
                                                 InlineKeyboardButton(text='Расход', callback_data='spend'),
                                                 InlineKeyboardButton(text='Мои счета', callback_data='myaccounts')],
                                                [InlineKeyboardButton(text='Статистика', callback_data='statistics'),
                                                 InlineKeyboardButton(text='Настройки', callback_data='settings'),
                                                 InlineKeyboardButton(text='Премиум', callback_data='premium')]])
