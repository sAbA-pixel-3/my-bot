from sqlalchemy import String, Integer, Column, ForeignKey, Date, create_engine, Text, Table
from sqlalchemy.orm import relationship, sessionmaker, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs



class Base(AsyncAttrs, DeclarativeBase): 
    pass

class Dishes(Base):
    __tablename__ = "dishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text,  nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False) 


class SideDishes(Base):
    __tablename__ = "sidedishes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text,  nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


class Salads(Base):
    __tablename__ = "salads" 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text,  nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


class Drinks(Base):
    __tablename__ = "drinks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text,  nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


class Sauces(Base):
    __tablename__ = "sauces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text,  nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


class Deserts(Base):
    __tablename__ = "deserts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text,  nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)


from config import MYSQL_URL
engine = create_async_engine(MYSQL_URL, echo=True) 
async_session = async_sessionmaker(engine, expire_on_commit=False) 

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 