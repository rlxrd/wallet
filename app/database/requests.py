from app.database.models import Session
from app.database.models import Users, Currency, Accounts, TopUps, Spendings
from sqlalchemy import select


async def add_user_db(name, tg_id):
    with Session.begin() as session:
        user_query = session.scalar(select(Users.id).where(Users.tg_id == tg_id))
        if not user_query:
            session.add(Users(name=name, tg_id=tg_id))

        user_accounts = session.scalar(select(Accounts).where(Accounts.user == tg_id))
        session.commit()
        if not user_accounts:
            return False
        else:
            return True
        


def get_currencies_db():
    with Session.begin() as session:
        currencies_list = session.execute(select(Currency.id, Currency.name)).all()
        return currencies_list


def set_account_db(reg_data):
    with Session.begin() as session:
        try:
            user = session.execute(select(Users.id).where(Users.tg_id == reg_data['user'])).first()
            session.add(Accounts(name=reg_data['name'], currency=reg_data['currency'], user=user.id))
            session.commit()
            return True
        except:
            return False


def check_currency_db(currency):
    with Session.begin() as session:
        user = session.execute(select(Currency.id).where(Currency.id == currency)).first()
        if not user:
            return False
        else:
            return True
