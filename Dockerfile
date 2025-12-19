# Используем более конкретный и легковесный образ
FROM python:3.9-alpine

# Устанавливаем системные зависимости, необходимые для Tkinter и компиляции Python-пакетов
RUN apk add --no-cache \
    gcc \
    musl-dev \
    tk \
    tcl

WORKDIR /app

# Копируем зависимости отдельно для лучшего кэширования слоев Docker
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY src/ ./src/

# Указываем точку входа. Хорошая практика — использовать python -m для модулей.
CMD ["python", "-m", "src.main"]
