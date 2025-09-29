FROM python:3.11-slim

WORKDIR /app

COPY services/core_admin/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копіюємо код сервісу та спільний common
COPY services/core_admin ./core_admin
COPY services/common ./common

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uvicorn", "core_admin.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
