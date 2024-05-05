
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime

from utils.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    # Додавання зв'язку з моделлю SaleReceipt
    sale_receipts = relationship("SaleReceipt", back_populates="user")


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450),nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)