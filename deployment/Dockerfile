# Используем легкий образ Python
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем библиотеки (без кэша для уменьшения веса)
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код сервера и модель
COPY app.py .
# Важно: модель должна лежать в папке deployment перед сборкой!
COPY tuned_xgboost.pkl . 

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]