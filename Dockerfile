# Використання офіційного іміджу Python
FROM python:3.9-slim

# Встановлення залежностей для FastAPI
RUN pip install fastapi uvicorn[standard]

# Додавання файлів проєкту в контейнер
COPY ./app /app

# Встановлення PostgreSQL клієнта
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client

# Встановлення додаткових залежностей (за необхідності)
RUN pip install -r /app/requirements.txt

# Встановлення робочої директорії
WORKDIR /app

# Запуск FastAPI сервера через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]