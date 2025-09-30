FROM python:3.11-slim

WORKDIR /app

# Системні пакети
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*


COPY services/core_board/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/core_board ./core_board
COPY services/common ./common

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uvicorn", "core_board.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

