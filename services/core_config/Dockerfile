FROM python:3.11-slim

WORKDIR /app

COPY services/core_config/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/core_config ./core_config
COPY services/common ./common

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uvicorn", "core_config.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
