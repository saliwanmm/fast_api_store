from pydantic import BaseModel

# Клас-модель для отримання даних в запиті реєстрації
class UserCreate(BaseModel):
    name: str
    username: str
    password: str

# Клас-модель для повернення даних відповіді після реєстрації користувача
class UserResponse(BaseModel):
    name: str
    username: str
