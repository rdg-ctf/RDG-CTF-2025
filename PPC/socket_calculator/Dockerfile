FROM ubuntu:22.04

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Настройка рабочей директории
WORKDIR /home/server

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV COMPOSE_HTTP_TIMEOUT 180
ENV DOCKER_CLIENT_TIMEOUT 180
ENV PIP_ROOT_USER_ACTION ignore
ENV PIP_NO_CACHE_DIR 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# Копирование файлов
COPY requirements.txt .
COPY *.py .

# Установка зависимостей Python
RUN pip3 install --no-input -r requirements.txt

# Оптимизация для множественных подключений
EXPOSE 8000

# Запуск сервера с поддержкой множественных подключений
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "120", "server:app"]