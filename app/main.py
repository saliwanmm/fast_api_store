from fastapi import FastAPI
from routers import user_router, receipt_router


app=FastAPI()


# Включення роутера для роботи з ауторизацією користувачів(login, loguot, register, change pass, get users)
app.include_router(user_router.router, tags=["user_router"])

# Включення роутера для роботи з чеками (create receipts, get receipts, filtrations)
app.include_router(receipt_router.router, tags=["receipt_router"])
