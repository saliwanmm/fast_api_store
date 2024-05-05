from pydantic import BaseModel
from typing import List
import datetime

# Create Basemodel for models using pydentic
class UserCreate(BaseModel):
    name: str
    username: str
    password: str


class requestdetails(BaseModel):
    username:str
    password:str

        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class changepassword(BaseModel):
    username:str
    old_password:str
    new_password:str


class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime.datetime


# Sale receipt create schemas
class Product(BaseModel):
    name: str
    price: float
    quantity: int


class Payment(BaseModel):
    type: str  # Варіанти: "cash" або "cashless"
    amount: float


class SaleReceiptCreate(BaseModel):
    products: List[Product]
    payment: Payment


class SaleReceipt(BaseModel):
    id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


# Response receipt schemas
class ProductResponse(BaseModel):
    name: str
    price: float
    quantity: int
    total: float

class PaymentResponse(BaseModel):
    type: str
    amount: float

class SaleReceiptResponse(BaseModel):
    id: int
    products: List[ProductResponse]
    payment: PaymentResponse
    total: float
    rest: float
    created_at: datetime.datetime
    owner_user: str
