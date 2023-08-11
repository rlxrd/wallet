from app.database.models import async_session as session
from app.database.models import Users, Currency, Accounts, TopUps, Spendings, Categories, Directions
from sqlalchemy import select, update, delete
from datetime import datetime

""" 
Внимание! Требует внесения корректировок для оптимизации.
"""

# Создание юзера при команде старт и проверка на наличие хоть одного созданного счета.
async def add_user_db(u_id):
    user_query = await session.scalar(select(Users).where(Users.tg_id == u_id))
    
    if not user_query:
        session.add(Users(tg_id=u_id))
        await session.commit()
        return False
    
    user_accounts = await session.scalar(select(Accounts.id).where(Accounts.user == user_query.id))
    if not user_accounts:
        return False
    return True


# Получение валют
async def get_currencies_db():
    currencies_list = await session.scalars(select(Currency))
    return currencies_list


# Создание счета
async def set_account_db(reg_data):
    try:
        user_d = await session.scalar(select(Users).where(Users.tg_id == reg_data['user']))
        currency_d = await session.scalar(select(Currency).where(Currency.id == reg_data['currency']))
        session.add(Accounts(name=reg_data['name'], balance=reg_data['amount'], currency=currency_d.id, user=user_d.id))
        await session.commit()
        return True
    except:
        return False


async def check_currency_db(currency):
    currency_data = await session.scalar(select(Currency).where(Currency.id == currency))
    if not currency_data:
        return False
    return currency_data


async def fetch_accounts_db(tg_id):
    user_d = await session.scalar(select(Users).where(Users.tg_id == tg_id))
    accounts_d = await session.scalars(select(Accounts).where(Accounts.user == user_d.id))
    return accounts_d


async def check_account_db(account):
    account_data = await session.scalar(select(Accounts).where(Accounts.id == account))
    if not account_data:
        return False
    else:
        return account_data


async def get_categories(direct):
        categories = await session.scalars(select(Categories).where(Categories.direct == direct))
        return categories


async def check_categories(direct):
    categories = await session.scalars(select(Categories).where(Categories.id == direct))
    if not categories:
        return False
    return categories


async def get_directions(cat):
    directions = await session.execute(select(Directions.id, Directions.name).where(Directions.category == cat))
    if not directions:
        return False
    return directions


async def update_balance_top(tdata):
    account = await session.scalar(select(Accounts).where(Accounts.id == tdata["account"]))
    direction = await session.scalar(select(Directions).where(Directions.id == tdata["direction"]))
    session.add(TopUps(date=datetime.now(), amount=tdata["amount"], account=account.id, direction=direction.id))
    await session.execute(update(Accounts).where(Accounts.id == account.id).values(balance=(account.balance + float(tdata["amount"]))))
    await session.commit()


async def update_balance_down(tdata):
    account = await session.scalar(select(Accounts).where(Accounts.id == tdata["account"]))
    direction = await session.scalar(select(Directions).where(Directions.id == tdata["direction"]))
    session.add(Spendings(date=datetime.now(), amount=tdata["amount"], account=account.id, direction=direction.id))
    await session.execute(update(Accounts).where(Accounts.id == account.id).values(balance=(account.balance - float(tdata["amount"]))))
    await session.commit()

        
async def fetch_my_accounts_db(tg_id):
    user_d = await session.scalar(select(Users).where(Users.tg_id == tg_id))
    accounts_d = await session.execute(select(Accounts.id, Accounts.user, Accounts.name, Accounts.balance, Accounts.currency).where(Accounts.user == user_d.id))
    return accounts_d


async def delete_acc(acc_id):
        await session.execute(delete(Accounts).where(Accounts.id == acc_id["account"]))
        await session.commit()


"""КОМАНДЫ
ДЛЯ АДМИНИСТРАТОРОВ
"""

async def add_currency_db(data):
        session.add(Currency(name=data["name"], code=data["code"]))
        await session.commit()
