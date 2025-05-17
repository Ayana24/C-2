# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости для PostgreSQL
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app/

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Открываем порт 8000
EXPOSE 8000

# Запускаем сервер через gunicorn
CMD ["gunicorn", "fstr_project.wsgi:application", "--bind", "0.0.0.0:8000"]
