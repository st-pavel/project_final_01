import pandas as pd
import joblib
from flask import Flask, request, jsonify

# Загружаем модель (нужно убедиться, что файл лежит рядом или путь указан верно)
# Мы используем лучшую модель из проекта
MODEL_PATH = 'tuned_xgboost.pkl'

try:
    model = joblib.load(MODEL_PATH)
    print(f"Модель {MODEL_PATH} успешно загружена.")
except Exception as e:
    print(f"Ошибка загрузки модели: {e}")
    model = None

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "model_loaded": model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # 1. Получаем JSON данные
        data = request.get_json()
        
        # 2. Превращаем в DataFrame (Pipeline требует имена колонок!)
        # Если пришел один объект, оборачиваем в список
        if isinstance(data, dict):
            data = [data]
        
        df = pd.DataFrame(data)
        
        # 3. Принудительная типизация (важно для пайплайна)
        # Zipcode должен быть строкой для TargetEncoder
        if 'zipcode' in df.columns:
            df['zipcode'] = df['zipcode'].astype(str)
            
        # 4. Предсказание
        prediction = model.predict(df)
        
        # 5. Возвращаем ответ
        return jsonify({
            "prediction": float(round(prediction[0], 2)),
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 400

if __name__ == '__main__':
    # host='0.0.0.0' обязателен для Docker!
    app.run(host='0.0.0.0', port=5000)