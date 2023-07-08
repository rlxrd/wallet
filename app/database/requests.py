from app.database.models import Session
from app.database.models import Users, Currency, Accounts, TopUps
from sqlalchemy import insert, select

async def add_user_db(name, tg_id):
    with Session.begin() as session:
        user_query = session.execute(select(Users).filter_by(tg_id=tg_id)).all()
        if not user_query:
            session.add(Users(name=name, tg_id=tg_id))
            session.commit()
