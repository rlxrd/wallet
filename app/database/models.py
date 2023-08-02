from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.orm import sessionmaker
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
    tg_id: Mapped[int]
    is_premium: Mapped[bool] = mapped_column(default=False)
    actived: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now(), onupdate=datetime.datetime.now())


class Currency(Base):
    __tablename__ = 'currencies'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(5))
    code: Mapped[str] = mapped_column(String(5))


class Accounts(Base):
    __tablename__ = 'accounts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String(19))
    balance: Mapped[float]
    currency: Mapped[int] = mapped_column(ForeignKey('currencies.id', ondelete='CASCADE'))


class Categories(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    direct: Mapped[bool]


class Directions(Base):
    __tablename__ = 'directions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))


class TopUps(Base):
    __tablename__ = 'topups'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.datetime] = mapped_column()
    amount: Mapped[float]
    account: Mapped[int] = mapped_column(ForeignKey('accounts.id', ondelete='CASCADE'))
    direction: Mapped[int] = mapped_column(ForeignKey('directions.id', ondelete='CASCADE'))


class Spendings(Base):
    __tablename__ = 'spendings'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column()
    account: Mapped[int] = mapped_column(ForeignKey('accounts.id', ondelete='CASCADE'))
    direction: Mapped[int] = mapped_column(ForeignKey('directions.id', ondelete='CASCADE'))


async def db_main():
    Base.metadata.create_all(bind=engine)
