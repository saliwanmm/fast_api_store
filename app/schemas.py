from pydantic import BaseModel
import datetime

# Create Basemodel for models using pydentic
class UserCreate(BaseModel):
    name: str
    username: str
    password: str

# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str

class requestdetails(BaseModel):
    username:str
    password:str

# class requestdetails(BaseModel):
#     email:str
#     password:str
        
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class changepassword(BaseModel):
    username:str
    old_password:str
    new_password:str

# class changepassword(BaseModel):
#     email:str
#     old_password:str
#     new_password:str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime.datetime