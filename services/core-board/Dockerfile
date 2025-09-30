FROM python:3.11-slim

WORKDIR /app

# Системні пакети
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Встановлення залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо код сервісу
COPY ./app ./app
COPY ./common ./common

# Expose порту
EXPOSE 8000

# Запуск uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
