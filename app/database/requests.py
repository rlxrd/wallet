from app.database.models import Session
from app.database.models import Users, Currency, Accounts, TopUps, Spendings, Categories, Directions
from sqlalchemy import select, update
import datetime


# Создание юзера при команде старт и проверка на наличие хоть одного созданного счета.
async def add_user_db(tg_id):
    with Session.begin() as session:
        user_query = session.scalar(select(Users.id).where(Users.tg_id == tg_id))
        if not user_query:
            session.add(Users(tg_id=tg_id))

        user_accounts = session.scalar(select(Accounts.id).where(Accounts.user == user_query))
        session.commit()
        if not user_accounts:
            return False
        return True


def get_currencies_db():
    with Session.begin() as session:
        currencies_list = session.execute(select(Currency.id, Currency.name)).all()
        return currencies_list


# Создание счета
def set_account_db(reg_data):
    with Session.begin() as session:
        try:
            user_d = session.execute(select(Users.id).where(Users.tg_id == reg_data['user'])).first()
            currency_d = session.execute(select(Currency.id).where(Currency.id == reg_data['currency'])).first()
            session.add(Accounts(name=reg_data['name'], balance=reg_data['amount'], currency=currency_d.id, user=user_d.id))
            session.commit()
            return True
        except:
            return False


def check_currency_db(currency):
    with Session.begin() as session:
        user = session.execute(select(Currency.id, Currency.name).where(Currency.id == currency)).first()
        if not user:
            return False
        return user


def fetch_accounts_db(tg_id):
    with Session.begin() as session:
        user_d = session.execute(select(Users.id).where(Users.tg_id == tg_id)).first()
        accounts_d = session.execute(select(Accounts.id, Accounts.name).where(Accounts.user == user_d.id)).all()
        return accounts_d


def check_account_db(account):
    with Session.begin() as session:
        account_data = session.execute(select(Accounts.id, Accounts.name, Accounts.balance, Accounts.currency).where(Accounts.id == account)).first()
        if not account:
            return False
        else:
            return account_data


def get_categories(direct):
    with Session.begin() as session:
        categories = session.execute(select(Categories.id, Categories.name).where(Categories.direct == direct)).all()
        return categories


def check_categories(direct):
    with Session.begin() as session:
        categories = session.execute(select(Categories).where(Categories.id == direct)).all()
        if not categories:
            return False
        return categories


def get_directions(cat):
    with Session.begin() as session:
        directions = session.execute(select(Directions.id, Directions.name).where(Directions.category == cat))
        if not directions:
            return False
        return directions


def update_balance_top(tdata):
    with Session.begin() as session:
        account = session.execute(select(Accounts.id, Accounts.balance).where(Accounts.id == tdata["account"])).first()
        direction = session.execute(select(Directions.id).where(Directions.id == tdata["direction"])).first()
        session.add(TopUps(date=datetime.datetime.now(), amount=tdata["amount"], account=account.id, direction=direction.id))
        session.execute(update(Accounts).where(Accounts.id == account.id).values(balance=(account.balance + int(tdata["amount"]))))
        session.commit()


def update_balance_down(tdata):
    with Session.begin() as session:
        account = session.execute(select(Accounts.id, Accounts.balance).where(Accounts.id == tdata["account"])).first()
        direction = session.execute(select(Directions.id).where(Directions.id == tdata["direction"])).first()
        session.add(Spendings(date=datetime.datetime.now(), amount=tdata["amount"], account=account.id, direction=direction.id))
        session.execute(update(Accounts).where(Accounts.id == account.id).values(balance=(account.balance - int(tdata["amount"]))))
        session.commit()

        
def fetch_my_accounts_db(tg_id):
    with Session.begin() as session:
        user_d = session.execute(select(Users.id).where(Users.tg_id == tg_id)).first()
        accounts_d = session.execute(select(Accounts.user, Accounts.name, Accounts.balance, Accounts.currency).where(Accounts.user == user_d.id)).all()
        return accounts_d


def all_stats(tg_id):
    with Session.begin() as session:
        history_list = []
        user = session.execute(select(Users.id).where(Users.tg_id == tg_id)).first()
        accounts = session.execute(select(Accounts.id).where(Accounts.user == user.id)).all()
        for acc in accounts:
            topups = session.execute(select(TopUps.id, TopUps.date, TopUps.amount, TopUps.account, TopUps.direction).where(TopUps.account == acc.id)).all()
            spendings = session.execute(select(Spendings.id, Spendings.date, Spendings.amount, Spendings.account, Spendings.direction).where(Spendings.account == acc.id)).all()
            history_list.append(topups)
            history_list.append(spendings)
        return history_list


"""КОМАНДЫ
ДЛЯ АДМИНИСТРАТОРОВ
"""

def add_direction_db(dir_name):
    with Session.begin() as session:
        session.add(Directions(name=dir_name))
        session.commit()
