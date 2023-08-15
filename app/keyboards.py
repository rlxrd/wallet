from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import (fetch_accounts_db, get_currencies_db,
                                   get_categories, get_directions,
                                   fetch_my_accounts_db, check_currency_db)


# Требует внесения корректировок
async def all_currencies_kb():
    currencies = await get_currencies_db()
    
    cur_kb = InlineKeyboardBuilder()
    for cur in currencies:
        cur_kb.add(InlineKeyboardButton(text=f'{cur.name} | {cur.code}', callback_data=str(cur.id)))
    cur_kb.adjust(3)
    return cur_kb.as_markup()


main_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬆️ Пополнение', callback_data='topup'),
                                                InlineKeyboardButton(text='⬇️ Расход', callback_data='spend')],
                                                [InlineKeyboardButton(text='💳 Мои счета', callback_data='myaccounts'),
                                                InlineKeyboardButton(text='📈 Статистика', callback_data='statistics')],
                                                [InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings'),
                                                InlineKeyboardButton(text='🌟 Премиум', callback_data='premium')]])


async def users_accounts_kb(tg_id):
    accounts = await fetch_accounts_db(tg_id)
    akbs = [[InlineKeyboardButton(text=acc.name, callback_data=str(acc.id))] for acc in accounts]
    akbs.append([InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')])
    accounts_kb = InlineKeyboardMarkup(inline_keyboard=akbs)
    return accounts_kb


sure = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='✅ Подтвердить', callback_data='yesyes')],
                                             [InlineKeyboardButton(text='❌ Отмена', callback_data='nono')]])


async def categiroes_kb(direct):
    all_categiroes = await get_categories(direct)
    ckbs = InlineKeyboardBuilder()
    for cat in all_categiroes:
        ckbs.add(InlineKeyboardButton(text=cat.name, callback_data=str(cat.id)))
    ckbs.add(InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    ckbs.adjust(1)
    return ckbs.as_markup()


async def directions_kb(cat):
    all_directs = await get_directions(cat)
    directs = InlineKeyboardBuilder()
    for dir in all_directs:
        directs.add(InlineKeyboardButton(text=dir.name, callback_data=str(dir.id)))
    directs.add(InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
    directs.adjust(2)
    return directs.as_markup()


async def my_accs(tg_id):
    accounts = await fetch_my_accounts_db(tg_id)
    print(accounts)
    kb = InlineKeyboardBuilder()
    for acc in accounts:
        print(acc)
        cur = await check_currency_db(acc[4])
        print(cur)
        try:
            kb.add(InlineKeyboardButton(text=f'{acc[2]} | {acc[3]} {cur.name}', callback_data=f'acc_{acc[0]}'))
        except:
            continue
    kb.add(InlineKeyboardButton(text='✅ Создать новый счёт', callback_data='add_new_acc'))
    kb.add(InlineKeyboardButton(text='◀️ Назад', callback_data='cancel'))
    kb.adjust(1)
    return kb.as_markup()


cancel_ikb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌ Отмена', callback_data='cancel')]])
back_ikb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='⬅️ Назад', callback_data='cancel')]])


async def acc_settings(acc_id):
    acc_setting = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌ Удалить счёт', callback_data=f'delete_{acc_id}')], [InlineKeyboardButton(text='◀️ Назад', callback_data='cancel')]])
    return acc_setting



