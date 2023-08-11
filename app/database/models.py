from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine
from datetime import datetime
import config

engine = create_async_engine(
    config.SQLALCHEMY_URL,
    echo=config.SQLALCHEMY_ECHO,
)
    
async_session = AsyncSession(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# Пользователи бота
class Users(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    is_premium: Mapped[bool] = mapped_column(default=False)


# Доступные валюты
class Currency(Base):
    __tablename__ = 'currencies'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(5))
    code: Mapped[str] = mapped_column(String(5))


# Счета пользователей
class Accounts(Base):
    __tablename__ = 'accounts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String(19))
    balance: Mapped[float]
    currency: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete='CASCADE'))


# Категории для пополнений и расходов
class Categories(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    direct: Mapped[bool]


# Направления для пополнения и расходов
class Directions(Base):
    __tablename__ = 'directions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))


# История пополнений
class TopUps(Base):
    __tablename__ = 'topups'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column()
    amount: Mapped[float]
    account: Mapped[int] = mapped_column(ForeignKey('accounts.id', ondelete='CASCADE'))
    direction: Mapped[int] = mapped_column(ForeignKey('directions.id', ondelete='CASCADE'))


# История списаний
class Spendings(Base):
    __tablename__ = 'spendings'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column()
    account: Mapped[int] = mapped_column(ForeignKey('accounts.id', ondelete='CASCADE'))
    direction: Mapped[int] = mapped_column(ForeignKey('directions.id', ondelete='CASCADE'))


# Создание всех таблиц (моделей)
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
