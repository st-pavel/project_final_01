import json

notebook_path = '/home/pavel/IDE/project_final_01/project_final_000.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Первичный анализ и очистка данных\n",
    "\n",
    "Проведем осмотр данных, проверим типы, наличие пропусков и дубликатов."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "data.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(f\"Размер датасета: {data.shape}\")\n",
    "duplicates = data.duplicated().sum()\n",
    "print(f\"Количество дубликатов: {duplicates} ({duplicates/len(data):.2%})\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Удаление дубликатов\n",
    "Дубликаты могут исказить результаты анализа и обучения модели. Удалим их."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "data = data.drop_duplicates()\n",
    "print(f\"Размер после удаления дубликатов: {data.shape}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Обработка целевой переменной (target)\n",
    "Целевая переменная сейчас в строковом формате (содержит '$' и ','). Преобразуем ее в число."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def clean_currency(x):\n",
    "    if isinstance(x, str):\n",
    "        return x.replace('$', '').replace(',', '').replace('+', '')\n",
    "    return x\n",
    "\n",
    "data['target'] = data['target'].apply(clean_currency)\n",
    "data['target'] = pd.to_numeric(data['target'], errors='coerce')\n",
    "\n",
    "print(\"Пропуски в target после очистки:\", data['target'].isna().sum())\n",
    "data.dropna(subset=['target'], inplace=True)\n",
    "print(f\"Размер после удаления пропусков в target: {data.shape}\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Очистка числовых признаков (sqft, beds, baths)\n",
    "Эти поля также содержат лишние символы."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# sqft\n",
    "def clean_sqft(x):\n",
    "    if isinstance(x, str):\n",
    "        # Удаляем 'sqft' и запятые\n",
    "        x = x.lower().replace('sqft', '').replace(',', '').strip()\n",
    "        if '-' in x: # обработка диапазонов, берем среднее или первое\n",
    "             return float('nan')\n",
    "    return x\n",
    "\n",
    "data['sqft'] = data['sqft'].apply(clean_sqft)\n",
    "data['sqft'] = pd.to_numeric(data['sqft'], errors='coerce')\n",
    "\n",
    "# beds\n",
    "def clean_beds(x):\n",
    "    if isinstance(x, str):\n",
    "        x = x.lower().replace('beds', '').replace('bd', '').strip()\n",
    "        # Можно добавить логику для '1-2 beds' и т.д.\n",
    "    return x\n",
    "\n",
    "data['beds'] = data['beds'].apply(clean_beds)\n",
    "# beds чаще всего целое, но бывают float (редко)\n",
    "data['beds'] = pd.to_numeric(data['beds'], errors='coerce')\n",
    "\n",
    "# baths\n",
    "def clean_baths(x):\n",
    "    if isinstance(x, str):\n",
    "        x = x.lower().replace('baths', '').replace('ba', '').strip()\n",
    "    return x\n",
    "\n",
    "data['baths'] = data['baths'].apply(clean_baths)\n",
    "data['baths'] = pd.to_numeric(data['baths'], errors='coerce')\n",
    "\n",
    "print(\"Info после очистки основных числовых полей:\")\n",
    "data[['sqft', 'beds', 'baths']].info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Анализ пропусков"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "missing = data.isnull().mean() * 100\n",
    "missing = missing[missing > 0].sort_values(ascending=False)\n",
    "plt.figure(figsize=(10, 6))\n",
    "sns.barplot(x=missing.index, y=missing.values, palette='viridis')\n",
    "plt.xticks(rotation=45)\n",
    "plt.title('Процент пропущенных значений по признакам')\n",
    "plt.ylabel('Процент пропусков')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Разведочный анализ данных (EDA)\n",
    "\n",
    "### Распределение целевой переменной (Price)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(10, 6))\n",
    "sns.histplot(data['target'], bins=50, kde=True)\n",
    "plt.title('Распределение стоимости недвижимости')\n",
    "plt.xlabel('Цена ($)')\n",
    "plt.show()\n",
    "\n",
    "print(\"Основные статистики Price:\")\n",
    "print(data['target'].describe())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Логарифмирование целевой переменной для нормализации распределения\n",
    "plt.figure(figsize=(10, 6))\n",
    "sns.histplot(np.log1p(data['target']), bins=50, kde=True, color='green')\n",
    "plt.title('Log-распределение стоимости')\n",
    "plt.xlabel('Log(Price)')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Корреляционный анализ (числовые признаки)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "corr_matrix = data[['target', 'sqft', 'beds', 'baths']].corr()\n",
    "plt.figure(figsize=(8, 6))\n",
    "sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')\n",
    "plt.title('Корреляция числовых признаков')\n",
    "plt.show()"
   ]
  }
]

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Notebook updated successfully.")
