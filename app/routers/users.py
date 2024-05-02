from fastapi import APIRouter, HTTPException, FastAPI, Depends, status
from sqlalchemy.orm import Session

from schemas.schemas import UserCreate, UserResponse
from models.user import User
from database.database import SessionLocal, engine, Base

router = APIRouter()

Base.metadata.create_all(engine)
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
app=FastAPI()

@router.post("/register/")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(username=user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")


    new_user = User(username=user.username, name=user.name)
    new_user.set_password(user.password)


    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Повернення відповіді з інформацією про створеного користувача
    return {"message":"user created successfully"}
