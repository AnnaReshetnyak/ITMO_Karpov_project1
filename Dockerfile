FROM python:3.9-slim

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*


COPY . .


# Настройка pip для ARM-совместимых пакетов
ENV PIP_DEFAULT_TIMEOUT=300 \
    PIP_RETRIES=10 \
    NO_CACHE_DIR=1

# Копирование и установка остальных зависимостей
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
