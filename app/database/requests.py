from app.database.models import async_session
from app.database.models import Users, Currency, Accounts, Transaction, Categories, Directions
from sqlalchemy import select, update, delete, desc
from datetime import datetime

""" 
Внимание! Требует внесения корректировок для оптимизации.
"""

# Создание юзера при команде старт и проверка на наличие хоть одного созданного счета.
async def add_user_db(u_id):
    async with async_session() as session:
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
    async with async_session() as session:
        currencies_list = await session.scalars(select(Currency))
    return currencies_list


# Создание счета
async def set_account_db(reg_data):
    async with async_session() as session:
        try:
            user_d = await session.scalar(select(Users).where(Users.tg_id == reg_data['user']))
            currency_d = await session.scalar(select(Currency).where(Currency.id == reg_data['currency']))
            session.add(Accounts(name=reg_data['name'], balance=reg_data['amount'], currency=currency_d.id, user=user_d.id))
            await session.commit()
            return True
        except:
            return False


async def check_currency_db(currency):
    async with async_session() as session:
        currency_data = await session.scalar(select(Currency).where(Currency.id == currency))
        if not currency_data:
            return False
    return currency_data


async def fetch_accounts_db(tg_id):
    async with async_session() as session:
        user_d = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        accounts_d = await session.scalars(select(Accounts).where(Accounts.user == user_d.id))
    return accounts_d


async def check_account_db(account):
    async with async_session() as session:
        account_data = await session.scalar(select(Accounts).where(Accounts.id == account))
        if not account_data:
            return False
        else:
            return account_data


async def get_categories(direct):
    async with async_session() as session:
        categories = await session.scalars(select(Categories).where(Categories.direct == direct))
    return categories


async def check_categories(direct):
    async with async_session() as session:
        categories = await session.scalars(select(Categories).where(Categories.id == direct))
        if not categories:
            return False
    return categories


async def get_directions(cat):
    async with async_session() as session:
        directions = await session.execute(select(Directions.id, Directions.name).where(Directions.category == cat))
        if not directions:
            return False
    return directions


async def update_balance(amount, account, direction, type):
    async with async_session() as session:
        account_data = await session.scalar(select(Accounts).where(Accounts.id == account))
        direction_data = await session.scalar(select(Directions).where(Directions.id == direction))
        session.add(Transaction(date=datetime.now().strftime("%Y-%m-%d %H:%M"), amount=amount, account=account_data.id, direction=direction_data.id, type=type))
        await session.execute(update(Accounts).where(Accounts.id == account_data.id).values(balance=(account_data.balance + float(amount)) if type else (account_data.balance - float(amount))))
        await session.commit()

        
async def fetch_my_accounts_db(tg_id):
    async with async_session() as session:
        user_d = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        accounts_d = await session.execute(select(Accounts.id, Accounts.user, Accounts.name, Accounts.balance, Accounts.currency).where(Accounts.user == user_d.id))
    return accounts_d


async def delete_acc(acc_id):
    async with async_session() as session:
        account = await session.scalar(select(Accounts).where(Accounts.id == acc_id["account"]))
        await session.delete(account)
        await session.commit()


async def get_all_stats(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        accounts = await session.scalars(select(Accounts).where(Accounts.user == user.id))
        if not accounts:
            return False
        transactions_all = {}
        for account in accounts:
            currency = await session.scalar(select(Currency.name).where(Currency.id == account.currency))
            transactions = await session.scalars(select(Transaction).where(Transaction.account == account.id).order_by(desc(Transaction.id)))
            for transaction in transactions:
                transactions_all[transaction.id] = f'{"🟢" if transaction.type else "🔴"} {transaction.date[-14:]} | {transaction.amount} {currency}'
    return dict(sorted(transactions_all.items(), key=lambda item: item[0])[-10:])
        

"""КОМАНДЫ
ДЛЯ АДМИНИСТРАТОРОВ
"""

async def add_currency_db(data):
    async with async_session() as session:
        session.add(Currency(name=data["name"], code=data["code"]))
        await session.commit()
