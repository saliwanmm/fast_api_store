import jwt
import ast

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from functools import wraps
from datetime import datetime

import utils.schemas as schemas
import models.usermodel as usermodel
from models.usermodel import User, TokenTable
from utils.database import Base, engine, SessionLocal
from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from utils.auth_bearer import JWTBearer
from models.salereceiptmodel import SaleReceipt
from utils.schemas import SaleReceiptCreate
from models.salereceiptmodel import SaleReceipt as DBSaleReceipt
from models.usermodel import User as DBUser


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
app=FastAPI()


@app.post("/register")
def register_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(usermodel.User).filter_by(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    encrypted_password =get_hashed_password(user.password)

    new_user = usermodel.User(name=user.name, username=user.username, password=encrypted_password )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message":"user created successfully"}

@app.post('/login' ,response_model=schemas.TokenSchema)
def login(request: schemas.requestdetails, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.username == request.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access=create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = usermodel.TokenTable(user_id=user.id,  access_token=access,  refresh_token=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }

@app.get('/getusers')
def getusers( dependencies=Depends(JWTBearer()),session: Session = Depends(get_session)):
    user = session.query(usermodel.User).all()
    return user

@app.post('/change-password')
def change_password(request: schemas.changepassword, db: Session = Depends(get_session)):
    user = db.query(usermodel.User).filter(usermodel.User.username == request.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password")
    
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    db.commit()
    
    return {"message": "Password changed successfully"}

@app.post('/logout')
def logout(dependencies=Depends(JWTBearer()), db: Session = Depends(get_session)):
    token=dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    token_record = db.query(usermodel.TokenTable).all()
    info=[]
    for record in token_record :
        print("record",record)
        if (datetime.utcnow() - record.created_date).days >1:
            info.append(record.user_id)
    if info:
        existing_token = db.query(usermodel.TokenTable).where(TokenTable.user_id.in_(info)).delete()
        db.commit()
        
    existing_token = db.query(usermodel.TokenTable).filter(usermodel.TokenTable.user_id == user_id, usermodel.TokenTable.access_token==token).first()
    if existing_token:
        existing_token.status=False
        db.add(existing_token)
        db.commit()
        db.refresh(existing_token)
    return {"message":"Logout Successfully"} 

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
    
        payload = jwt.decode(kwargs['dependencies'], JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        data= kwargs['session'].query(usermodel.TokenTable).filter_by(user_id=user_id,access_token=kwargs['dependencies'],status=True).first()
        if data:
            return func(kwargs['dependencies'],kwargs['session'])
        
        else:
            return {'msg': "Token blocked"}
        
    return wrapper


def verify_token(token: str = Depends(JWTBearer())):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# Ендпоінт для створення чеку продажу з перевіркою авторизації
@app.post("/sale_receipts/", response_model=schemas.SaleReceipt)
def create_sale_receipt(
    sale_receipt: schemas.SaleReceiptCreate,
    current_user: int = Depends(verify_token),  # Викликаємо функцію перевірки авторизації
    db: Session = Depends(get_session)
):
    # Обчислення додаткової інформації про чек
    total_amount = sum(item.price * item.quantity for item in sale_receipt.products)
    rest_amount = sale_receipt.payment.amount - total_amount

    # Збереження чеку продажу в базі даних
    db_sale_receipt = DBSaleReceipt(
        user_id=current_user,
        products=str(sale_receipt.products),
        payment_type=sale_receipt.payment.type,
        payment_amount=sale_receipt.payment.amount,
        total_amount=total_amount,
        rest_amount=rest_amount
    )

    db.add(db_sale_receipt)
    db.commit()
    db.refresh(db_sale_receipt)

    return db_sale_receipt


@app.get("/sale_receipts/{receipt_id}", response_model=schemas.SaleReceiptResponse)
def get_sale_receipt(
    receipt_id: int,
    current_user: int = Depends(verify_token),
    db: Session = Depends(get_session)
):
    db_receipt = db.query(DBSaleReceipt).filter(DBSaleReceipt.id == receipt_id).first()
    if not db_receipt:
        raise HTTPException(status_code=404, detail="Sale receipt not found")

    products_string = db_receipt.products

   # Використання eval для перетворення рядка в об'єкти Python
    products_list = eval(products_string)

    # Створити список словників для продуктів
    products_dict_list = []
    for product_data in products_list:
        # Отримати дані про кожен продукт і створити словник
        product_dict = {
            "name": product_data.name,
            "price": product_data.price,
            "quantity": product_data.quantity,
            "total": product_data.price * product_data.quantity
        }
        products_dict_list.append(product_dict)

    payment_data = {
        "type": db_receipt.payment_type,
        "amount": db_receipt.payment_amount
    }

    owner_user = db.query(DBUser).filter(DBUser.id == current_user).first()
    if not owner_user:
        raise HTTPException(status_code=404, detail="User owner receipt not found")


    response_data = {
        "id": db_receipt.id,
        "products": products_dict_list,
        "payment": payment_data,
        "total": db_receipt.total_amount,
        "rest": db_receipt.rest_amount,
        "created_at": db_receipt.created_at,
        "user_id": owner_user.name
    }

    return response_data