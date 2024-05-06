import json

from fastapi import APIRouter
from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from utils.utils import verify_token
import utils.schemas as schemas
from utils.session import get_session
from models.usermodel import User as DBUser
from models.salereceiptmodel import SaleReceipt as DBSaleReceipt


router = APIRouter()


# Ендпоінт для створення чеку продажу з перевіркою авторизації
@router.post("/sale_receipts/", response_model=schemas.SaleReceipt)
def create_sale_receipt(
    sale_receipt: schemas.SaleReceiptCreate,
    current_user: int = Depends(verify_token),  # Викликаємо функцію перевірки авторизації
    db: Session = Depends(get_session)
):
    # Обчислення додаткової інформації про чек
    total_amount = sum(item.price * item.quantity for item in sale_receipt.products)
    rest_amount = sale_receipt.payment.amount - total_amount

    # Перетворення products у формат JSON
    products_json = json.dumps([item.dict() for item in sale_receipt.products])

    # Збереження чеку продажу в базі даних
    db_sale_receipt = DBSaleReceipt(
        user_id=current_user,
        products=products_json,
        payment_type=sale_receipt.payment.type,
        payment_amount=sale_receipt.payment.amount,
        total_amount=total_amount,
        rest_amount=rest_amount
    )

    db.add(db_sale_receipt)
    db.commit()
    db.refresh(db_sale_receipt)

    return db_sale_receipt


# Ендпоінт для отримання чеку продаж за його ідентифікатором авторизованим користувачем
@router.get("/sale_receipts/{receipt_id}", response_model=schemas.SaleReceiptResponse)
def get_sale_receipt(
    receipt_id: int,
    current_user: int = Depends(verify_token),
    db: Session = Depends(get_session)
):
    # Знайти чек за його ID
    db_receipt = db.query(DBSaleReceipt).filter(DBSaleReceipt.id == receipt_id).first()
    if not db_receipt:
        raise HTTPException(status_code=404, detail="Sale receipt not found")

    # Перевірка чи користувач, який залогінений, створив цей рецепт
    if int(db_receipt.user_id) != int(current_user):
        raise HTTPException(status_code=403, detail="Unauthorized to access this sale receipt")

   # Парсинг рядка продуктів у список словників
    products_list = json.loads(db_receipt.products)
    
    # Створення списку продуктів з обчисленням загальної вартості
    products_dict_list = []
    for product_data in products_list:
        product_dict = {
            "name": product_data.get('name', ''),
            "price": product_data.get('price', 0),
            "quantity": product_data.get('quantity', 0),
            "total": product_data.get('price', 0) * product_data.get('quantity', 0)
        }
        products_dict_list.append(product_dict)

    # Дані про оплату
    payment_data = {
        "type": db_receipt.payment_type,
        "amount": db_receipt.payment_amount
    }

    # Знайти користувача, який створив цей чек (по його user_id)
    owner_user = db.query(DBUser).filter(DBUser.id == db_receipt.user_id).first()
    if not owner_user:
        raise HTTPException(status_code=404, detail="User owner receipt not found")


    response_data = {
        "id": db_receipt.id,
        "products": products_dict_list,
        "payment": payment_data,
        "total": db_receipt.total_amount,
        "rest": db_receipt.rest_amount,
        "created_at": db_receipt.created_at,
        "owner_user": owner_user.name
    }

    return response_data


# Ендпоінт для отримання списку чеків продаж за різними фільтрами авторизованим користувачем
@router.get("/get_receipts", response_model=list[schemas.SaleReceiptResponse])
def get_sale_receipt(
    current_user: int = Depends(verify_token),
    total_amount: Optional[float] = None,
    payment_type: Optional[str] = None,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: Optional[int] = Query(10, ge=1, le=100),
    page: Optional[int] = Query(1, ge=1),
    offset: Optional[int] = Query(None, ge=0),
    db: Session = Depends(get_session)
):

    # Отримання всіх рецептів продаж, створених поточним користувачем
    query = db.query(DBSaleReceipt).filter(DBSaleReceipt.user_id == current_user)

    # Задаємо фільтрацію по загальній сумі оплати
    if total_amount is not None:
        query = query.filter(DBSaleReceipt.total_amount > total_amount)
    
    # Задаємо фільтрацію по типу оплати
    if payment_type is not None:
        query = query.filter(DBSaleReceipt.payment_type == payment_type)

    # Задаємо початкову дату фільтрації
    if start_date is not None:
        query = query.filter(DBSaleReceipt.created_at >= start_date)
    
    # Задаємо кінцеву дату фільтрації
    if end_date is not None:
        query = query.filter(DBSaleReceipt.created_at <= end_date)

    # Використовуємо limit для обмеження кількості записів на сторінці
    if limit:
        query = query.limit(limit)

    # Використовуємо offset для пропуску перших записів у вибірці
    if offset:
        query = query.offset(offset)

    db_receipt_list = query.all()

    response_data_list = []

    # Перебираємо список чеків продаж
    for db_receipt in db_receipt_list:

        # Парсинг рядка продуктів у список словників
        products_list = json.loads(db_receipt.products)
        
        # Створення списку продуктів з обчисленням загальної вартості
        products_dict_list = []
        for product_data in products_list:
            product_dict = {
                "name": product_data.get('name', ''),
                "price": product_data.get('price', 0),
                "quantity": product_data.get('quantity', 0),
                "total": product_data.get('price', 0) * product_data.get('quantity', 0)
            }
            products_dict_list.append(product_dict)

        # Дані про оплату
        payment_data = {
            "type": db_receipt.payment_type,
            "amount": db_receipt.payment_amount
        }

        # Знайти користувача, який створив цей чек (по його user_id)
        owner_user = db.query(DBUser).filter(DBUser.id == db_receipt.user_id).first()
        if not owner_user:
            raise HTTPException(status_code=404, detail="User owner receipt not found")

        response_data = {
            "id": db_receipt.id,
            "products": products_dict_list,
            "payment": payment_data,
            "total": db_receipt.total_amount,
            "rest": db_receipt.rest_amount,
            "created_at": db_receipt.created_at,
            "owner_user": owner_user.name
        }

        response_data_list.append(response_data)

    return response_data_list
