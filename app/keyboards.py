from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.database.requests import *


def all_currencies_kb() -> InlineKeyboardMarkup:
    currencies = get_currencies_db()
    
    currencies_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=currency.name, callback_data=currency.id)] for currency in currencies])   
    return currencies_kb
