
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime

# from database import Base
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     username = Column(String(50), nullable=False)
#     email = Column(String(100), unique=True, nullable=False)
#     password = Column(String(100), nullable=False)


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)