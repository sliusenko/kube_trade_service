FROM python:3.11-slim

WORKDIR /app

COPY services/core_news/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копіюємо код сервісу та спільний common
COPY services/core_news ./core_news
COPY services/common ./common

CMD ["uvicorn", "core_news.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
