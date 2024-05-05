from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from utils.database import Base
import datetime


# Модель для чеку продажу
class SaleReceipt(Base):
    __tablename__ = "sale_receipts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Зв'язок з ідентифікатором користувача
    products = Column(JSON, nullable=False)
    payment_type = Column(String(50), nullable=False)
    payment_amount = Column(Float)
    total_amount = Column(Float)
    rest_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.now)

    # Зв'язок з таблицею користувачів (один до багатьох)
    user = relationship("User", back_populates="sale_receipts")