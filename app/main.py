from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database.database import engine, SessionLocal

from routers import items, users

# Створення екземпляру додатка FastAPI
app = FastAPI()

# Налаштування Jinja2 для зчитування шаблонів з папки templates
templates = Jinja2Templates(directory="templates")

# Налаштування StaticFiles для зчитування статичних файлів з папки static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Опис кореневого маршруту
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Hello BRO!"})

# Включення роутера з предметами (якщо це потрібно)
app.include_router(items.router, tags=["items"])

# Включення роутера для реєстрації користувачів
app.include_router(users.router, tags=["register"])