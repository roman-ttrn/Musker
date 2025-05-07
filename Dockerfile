# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app/src
WORKDIR /app/src

# Сначала копируем только requirements.txt
COPY --chown=appuser:appuser requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем остальной код
COPY --chown=appuser:appuser . .

# Команда для запуска (collectstatic лучше делать здесь)
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn your_project.wsgi:application --bind 0.0.0.0:8000"]