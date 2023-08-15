from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime
from typing import List
import config

engine = create_async_engine(
    config.SQLALCHEMY_URL,
    echo=config.SQLALCHEMY_ECHO,
)
    
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# Пользователи бота
class Users(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    is_premium: Mapped[bool] = mapped_column(default=False)
    
    account_rel: Mapped[List["Accounts"]] = relationship(back_populates="user_rel", cascade='all, delete')


# Доступные валюты
class Currency(Base):
    __tablename__ = 'currencies'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(5))
    code: Mapped[str] = mapped_column(String(5))
    
    account_rel: Mapped[List["Accounts"]] = relationship(back_populates="currency_rel", cascade='all, delete')


# Счета пользователей
class Accounts(Base):
    __tablename__ = 'accounts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String(19))
    balance: Mapped[float]
    currency: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete='CASCADE'))
    
    user_rel: Mapped["Users"] = relationship(back_populates="account_rel")
    currency_rel: Mapped["Currency"] = relationship(back_populates="account_rel")
    
    transaction_rel: Mapped[List["Transaction"]] = relationship(back_populates="account_rel", cascade='all, delete')


# Категории для пополнений и расходов
class Categories(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    direct: Mapped[bool]
    
    directions_rel: Mapped[List["Directions"]] = relationship(back_populates="category_rel", cascade='all, delete')


# Направления для пополнения и расходов
class Directions(Base):
    __tablename__ = 'directions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    
    category_rel: Mapped["Categories"] = relationship(back_populates="directions_rel")
    transaction_rel: Mapped["Transaction"] = relationship(back_populates="direction_rel", cascade='all, delete')


# История пополнений
class Transaction(Base):
    __tablename__ = 'transaction'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    amount: Mapped[float]
    account: Mapped[int] = mapped_column(ForeignKey('accounts.id', ondelete='CASCADE'))
    direction: Mapped[int] = mapped_column(ForeignKey('directions.id', ondelete='CASCADE'))
    type: Mapped[bool]
    
    account_rel: Mapped["Accounts"] = relationship(back_populates="transaction_rel")
    direction_rel: Mapped["Directions"] = relationship(back_populates="transaction_rel")



# Создание всех таблиц (моделей)
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
