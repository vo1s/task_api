# Используем Python 3.11
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /task_api/task_api/

# Копируем файлы
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт
EXPOSE 8000
