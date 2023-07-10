from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.orm import sessionmaker, relationship
import datetime

import config

engine = create_engine(url=config.SQLALCHEMY_URL,
                       echo=config.SQLALCHEMY_ECHO)

Session = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(35))
    tg_id: Mapped[int] = mapped_column()
    is_premium: Mapped[bool] = mapped_column(default=False)


class Currency(Base):
    __tablename__ = 'currencies'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(35))
    code: Mapped[str] = mapped_column(String(5))


class Accounts(Base):
    __tablename__ = 'accounts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String(35))
    balance: Mapped[int]
    currency: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete='CASCADE'))


class Directions(Base):
    __tablename__ = 'directions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    direct: Mapped[int]


class TopUps(Base):
    __tablename__ = 'topups'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    amount: Mapped[int] = mapped_column()
    account: Mapped[int] = mapped_column(ForeignKey('accounts.id', ondelete='CASCADE'))
    direction: Mapped[int] = mapped_column(ForeignKey('directions.id', ondelete='CASCADE'))


class Spendings(Base):
    __tablename__ = 'spendings'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    amount: Mapped[int] = mapped_column()
    account: Mapped[int] = mapped_column(ForeignKey('accounts.id', ondelete='CASCADE'))
    direction: Mapped[int] = mapped_column(ForeignKey('directions.id', ondelete='CASCADE'))


async def db_main():
    Base.metadata.create_all(bind=engine)
