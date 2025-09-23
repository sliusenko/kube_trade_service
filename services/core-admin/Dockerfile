FROM python:3.11-slim

WORKDIR /app

# Встановлення залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код сервісу
COPY ./app ./app

EXPOSE 8000

# Запускаємо FastAPI через uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
