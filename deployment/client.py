import requests
import json

# URL вашего сервера (локальный или ngrok)
# Если запускаете локально через python app.py или docker:
URL = 'http://localhost:5000/predict'
# Если используете ngrok, вставьте ссылку сюда:
# URL = 'https://xxxx-xxxx.ngrok-free.app/predict'

# Данные для проверки (взяты из X_test)
sample_data = {
    "status": "for sale",
    "propertyType": "single family",
    "baths": 3.0,
    "zipcode": "27263",  # Важно: передаем как строку!
    "state": "NC",
    "latitude": 35.9359,
    "longitude": -79.9395,
    "sqft": 3382.0,
    "stories": 1.0,
    "beds": 4.0,
    "heating": "forced air",
    "cooling": "central",
    "parking": "attached",
    "lotsize": 22215.6,
    "age": 30.0,
    "age_remodeled": 30.0,
    "rating_mean": 4.5,
    "distance_mean": 1.63,
    "schools_count": 4.0
}

print(f"Отправка запроса на {URL}...")
print("-" * 30)

try:
    response = requests.post(URL, json=sample_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Успех!")
        print(f"Предсказанная стоимость: ${result['prediction']:,.2f}")
    else:
        print(f"Ошибка сервера ({response.status_code}):")
        print(response.text)
        
except Exception as e:
    print("Не удалось соединиться с сервером.")
    print(f"Детали: {e}")
    print("Проверьте, запущен ли Docker/Flask и верен ли URL.")