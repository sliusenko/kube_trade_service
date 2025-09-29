FROM python:3.11-slim

WORKDIR /app

COPY services/core_fetch/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# копіюємо код сервісу та спільний common
COPY services/core_fetch ./core_fetch
COPY services/common ./common

# Run FastAPI with uvicorn
CMD ["uvicorn", "core_fetch.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
