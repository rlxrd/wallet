from sqlalchemy import create_engine, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.orm import Session, sessionmaker

from datetime import datetime

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
    tg_id: Mapped[int]


class Currency(Base):
    __tablename__ = 'currencies'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(35))


class Accounts(Base):
    __tablename__ = 'accounts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(35))
    balance: Mapped[int]
    currency: Mapped[int] = mapped_column(ForeignKey('currencies.id'))


class TopUps(Base):
    __tablename__ = 'topups'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str]
    amount: Mapped[int]


async def db_main():
    Base.metadata.create_all(bind=engine)
