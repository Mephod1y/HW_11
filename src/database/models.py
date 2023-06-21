from sqlalchemy import Column, Integer, String, func
from sqlalchemy.sql.sqltypes import Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(40), nullable=False)
    email = Column(String(50), unique=True, index=True)
    phone = Column(Integer, unique=True, index=True)
    birthday = Column(Date, nullable=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)