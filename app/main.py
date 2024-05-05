from fastapi import FastAPI

from routers import user_router, receipt_router

app=FastAPI()


# Включення роутера з ауторизацією користувачів
app.include_router(user_router.router, tags=["user_router"])

# Ендпоінт для роботи з чеками (створення, фільтрація)
app.include_router(receipt_router.router, tags=["receipt_router"])
