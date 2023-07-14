from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import (fetch_accounts_db, get_currencies_db, get_categories, get_directions)


def all_currencies_kb():
    currencies = get_currencies_db()
    
    cur_kb = InlineKeyboardBuilder()
    for cur in currencies:
        cur_kb.add(InlineKeyboardButton(text=cur.name, callback_data=cur.id))
    cur_kb.adjust(4)
    return cur_kb.as_markup()


main_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬆️ Пополнение', callback_data='topup'),
                                                InlineKeyboardButton(text='⬇️ Расход', callback_data='spend')],
                                                [InlineKeyboardButton(text='💳 Мои счета', callback_data='myaccounts'),
                                                InlineKeyboardButton(text='📈 Статистика', callback_data='statistics')],
                                                [InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings'),
                                                InlineKeyboardButton(text='🌟 Премиум', callback_data='premium')]])


def users_accounts_kb(tg_id):
    accounts = fetch_accounts_db(tg_id)
    akbs = [[InlineKeyboardButton(text=acc.name, callback_data=acc.id)] for acc in accounts]
    akbs.append([InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')])
    accounts_kb = InlineKeyboardMarkup(inline_keyboard=akbs)
    return accounts_kb


sure = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅ Подтвердить', callback_data='yesyes')],
                                             [InlineKeyboardButton(text='❌ Отмена', callback_data='nono')]])


def categiroes_kb(direct):
    all_categiroes = get_categories(direct)
    ckbs = InlineKeyboardBuilder()
    for cat in all_categiroes:
        ckbs.add(InlineKeyboardButton(text=cat.name, callback_data=cat.id))
    ckbs.add(InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return ckbs.as_markup()


def directions_kb(cat):
    all_directs = get_directions(cat)
    directs = InlineKeyboardBuilder()
    for dir in all_directs:
        directs.add(InlineKeyboardButton(text=dir.name, callback_data=dir.id))
    directs.add(InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    return directs.as_markup()

