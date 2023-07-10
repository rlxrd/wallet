from app.database.models import Session
from app.database.models import Users, Currency, Accounts, TopUps, Spendings, Directions, Admins
from sqlalchemy import select, update


# Создание юзера при команде старт и проверка на наличие хоть одного созданного счета.
async def add_user_db(name, tg_id):
    with Session.begin() as session:
        user_query = session.scalar(select(Users.id).where(Users.tg_id == tg_id))
        if not user_query:
            session.add(Users(name=name, tg_id=tg_id))

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
        user = session.execute(select(Currency.id).where(Currency.id == currency)).first()
        if not user:
            return False
        return True


def fetch_accounts_db(tg_id):
    with Session.begin() as session:
        user_d = session.execute(select(Users.id).where(Users.tg_id == tg_id)).first()
        accounts_d = session.execute(select(Accounts.id, Accounts.name).where(Accounts.user == user_d.id)).all()
        return accounts_d


def fetch_account_db(acc_id):
    with Session.begin() as session:
        account = session.execute(select(Accounts.id).where(Accounts.id == acc_id)).first()
        if not account:
            return False
        return True


def fetch_directions_topup():
    with Session.begin() as session:
        direction = session.execute(select(Directions.name, Directions.id).where(Directions.direct == 1)).all()
        return direction


def fetch_directions_check(d_id):
    with Session.begin() as session:
        direction = session.execute(select(Directions.id).where(Directions.id == d_id)).all()
        if not direction:
            return False
        return True


def update_balance_db(data):
    with Session.begin() as session:
        account = session.execute(select(Accounts.id, Accounts.balance).where(Accounts.id == data['account'])).first()
        direction = session.execute(select(Directions.id).where(Directions.id == data['direction'])).first()
        session.execute(update(Accounts).where(Accounts.id == account.id).values(balance=account.balance+int(data['amount'])))
        session.add(TopUps(amount=data['amount'], account=account.id, direction=direction.id))
        session.commit()


"""КОМАНДЫ
ДЛЯ АДМИНИСТРАТОРОВ
"""

def fetch_admins():
    with Session.begin() as session:
        admin = session.scalars(select(Admins.tg_id)).all()
        return admin


def add_direction_db(dir_name):
    with Session.begin() as session:
        session.add(Directions(name=dir_name))
        session.commit()
