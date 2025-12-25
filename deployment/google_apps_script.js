// 1. Эта функция создает меню при открытии таблицы
function onOpen() {
    var ui = SpreadsheetApp.getUi();
    ui.createMenu('🏡 ML Оценка') // Название меню в верхней панели
        .addItem('Оценить активную строку', 'predictPrice') // Название пункта -> Имя функции
        .addToUi();
  }
  
  // 2. Основная функция предсказания
  function predictPrice() {
    var sheet = SpreadsheetApp.getActiveSheet();
    var row = sheet.getActiveCell().getRow();
    
    // Пропускаем заголовок (строка 1)
    if (row < 2) {
      Browser.msgBox("⚠️ Пожалуйста, выберите строку с данными (не заголовок).");
      return;
    }
  
    // --- НАСТРОЙКИ ---
    // Вставьте сюда ваш актуальный URL от ngrok + /predict
    var url = "https://pterocarpous-aviana-syndicalistic.ngrok-free.dev/predict"; 
    // -----------------
  
    // Собираем данные. Индексы колонок: A=1, B=2 ... S=19
    var payload = {
      "status":        sheet.getRange(row, 1).getValue(),
      "propertyType":  sheet.getRange(row, 2).getValue(),
      "baths":         sheet.getRange(row, 3).getValue(),
      "zipcode":       String(sheet.getRange(row, 4).getValue()), // Строка!
      "state":         sheet.getRange(row, 5).getValue(),
      "latitude":      sheet.getRange(row, 6).getValue(),
      "longitude":     sheet.getRange(row, 7).getValue(),
      "sqft":          sheet.getRange(row, 8).getValue(),
      "stories":       sheet.getRange(row, 9).getValue(),
      "beds":          sheet.getRange(row, 10).getValue(),
      "heating":       sheet.getRange(row, 11).getValue(),
      "cooling":       sheet.getRange(row, 12).getValue(),
      "parking":       sheet.getRange(row, 13).getValue(),
      "lotsize":       sheet.getRange(row, 14).getValue(),
      "age":           sheet.getRange(row, 15).getValue(),
      "age_remodeled": sheet.getRange(row, 16).getValue(),
      "rating_mean":   sheet.getRange(row, 17).getValue(),
      "distance_mean": sheet.getRange(row, 18).getValue(),
      "schools_count": sheet.getRange(row, 19).getValue()
    };
  
    var options = {
      "method": "post",
      "contentType": "application/json",
      "payload": JSON.stringify(payload),
      "muteHttpExceptions": true
    };
    
    // Визуальный эффект: пишем "Загрузка..."
    sheet.getRange(row, 20).setValue("⏳...");
  
    try {
      var response = UrlFetchApp.fetch(url, options);
      var responseCode = response.getResponseCode();
      var responseText = response.getContentText();
      
      if (responseCode === 200) {
        var json = JSON.parse(responseText);
        
        // Записываем цену в колонку T (20)
        var priceCell = sheet.getRange(row, 20);
        priceCell.setValue(json.prediction);
        
        // Красим в зеленый и форматируем как валюту
        priceCell.setBackground("#d9ead3"); 
        priceCell.setNumberFormat('$#,##0.00');
        
      } else {
        sheet.getRange(row, 20).setValue("Ошибка");
        Browser.msgBox("Ошибка сервера (" + responseCode + "): " + responseText);
      }
    } catch (e) {
      sheet.getRange(row, 20).setValue("Сбой");
      Browser.msgBox("Не удалось соединиться: " + e + "\nПроверьте, запущен ли ngrok.");
    }
  }