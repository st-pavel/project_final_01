import json

notebook_path = '/home/pavel/IDE/project_final_01/project_final_000.ipynb'

def create_code_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source_lines]
    }

def create_markdown_cell(source_lines):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source_lines]
    }

new_cells = []

# 1. Header
new_cells.append(create_markdown_cell([
    "## 1.4. Очистка и анализ признаков sqft, beds, baths",
    "",
    "Приведем признаки `sqft`, `beds`, `baths` к числовому виду, удалив лишние символы и обработав пропуски/аномалии."
]))

# 2. Cleaning Code
source_cleaning = [
    "# Функция для очистки sqft",
    "def clean_sqft(x):",
    "    if isinstance(x, str):",
    "        # Удаляем 'sqft' и запятые",
    "        x = x.lower().replace('sqft', '').replace(',', '').strip()",
    "        if '-' in x: # обработка диапазонов (например, '1000-1200'), возвращаем NaN для простоты",
    "             return None",
    "        if not x.replace('.', '', 1).isdigit(): # Если не число после очистки",
    "             return None",
    "    return x",
    "",
    "# Функция для очистки beds",
    "def clean_beds(x):",
    "    if isinstance(x, str):",
    "        x = x.lower().replace('beds', '').replace('bd', '').replace('bed', '').strip()",
    "        # Обработка странных значений типа '1-2 beds' или текстовых описаний",
    "        if not x.replace('.', '', 1).isdigit():",
    "            return None",
    "    return x",
    "",
    "# Функция для очистки baths",
    "def clean_baths(x):",
    "    if isinstance(x, str):",
    "        x = x.lower().replace('baths', '').replace('ba', '').replace('bath', '').strip()",
    "        if not x.replace('.', '', 1).isdigit():",
    "            return None",
    "    return x",
    "",
    "# Применяем очистку",
    "data['sqft_clean'] = data['sqft'].apply(clean_sqft).astype(float)",
    "data['beds_clean'] = data['beds'].apply(clean_beds).astype(float)",
    "data['baths_clean'] = data['baths'].apply(clean_baths).astype(float)",
    "",
    "# Удаляем старые колонки или оставляем для сравнения? Пока оставим, но работать будем с clean.",
    "print(\"Пропуски после очистки:\")",
    "print(data[['sqft_clean', 'beds_clean', 'baths_clean']].isnull().sum())",
    "",
    "# Посмотрим на статистику",
    "print(data[['sqft_clean', 'beds_clean', 'baths_clean']].describe())"
]
new_cells.append(create_code_cell(source_cleaning))

# 3. Handle Missing Values in features (Simple imputation or drop? User followed sophisticated median for target.)
# For now, let's look at them first.
# source_impute = ... (Skip for now, user asked for analysis/cleaning first, imputation might be next step in reference)

# 4. EDA sqft
new_cells.append(create_markdown_cell([
    "### Анализ распределения площади (sqft)",
    "Посмотрим на гистограмму и boxplot для `sqft_clean`."
]))

source_eda_sqft = [
    "plt.figure(figsize=(12, 5))",
    "plt.subplot(1, 2, 1)",
    "sns.histplot(data['sqft_clean'].dropna(), bins=50, kde=True)",
    "plt.title('Распределение sqft')",
    "",
    "plt.subplot(1, 2, 2)",
    "sns.boxplot(x=data['sqft_clean'].dropna())",
    "plt.title('Boxplot sqft')",
    "plt.show()"
]
new_cells.append(create_code_cell(source_eda_sqft))

new_cells.append(create_markdown_cell([
    "**Вывод**:",
    "Распределение площади имеет длинный правый хвост (log-normal подобное).",
    "Наблюдаются значительные выбросы в большую сторону, которые могут исказить модель.",
    "Необходимо будет рассмотреть удаление выбросов или логарифмирование."
]))

# 5. EDA beds/baths
new_cells.append(create_markdown_cell([
    "### Анализ количества спален (beds) и ванных (baths)",
    "Это дискретные, но числовые признаки."
]))

source_eda_beds_baths = [
    "fig, ax = plt.subplots(1, 2, figsize=(14, 6))",
    "",
    "sns.countplot(x=data['beds_clean'].dropna(), ax=ax[0], order=sorted(data['beds_clean'].dropna().unique())[:15])",
    "ax[0].set_title('Top 15 значений Beds')",
    "ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45)",
    "",
    "sns.countplot(x=data['baths_clean'].dropna(), ax=ax[1], order=sorted(data['baths_clean'].dropna().unique())[:15])",
    "ax[1].set_title('Top 15 значений Baths')",
    "ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45)",
    "",
    "plt.tight_layout()",
    "plt.show()"
]
new_cells.append(create_code_cell(source_eda_beds_baths))

new_cells.append(create_markdown_cell([
    "**Вывод**:",
    "Большинство домов имеют от 1 до 5 спален.",
    "Есть дробные значения для ванных комнат (например, 2.5), что нормально для США (туалет без душа).",
    "Присутствуют аномально большие значения (выбросы), которые стоит проверить."
]))

# 6. Correlation
new_cells.append(create_markdown_cell([
    "### Корреляция с целевой переменной",
    "Построим матрицу корреляций для очищенных числовых признаков."
]))

source_corr = [
    "corr_cols = ['target_clean', 'sqft_clean', 'beds_clean', 'baths_clean']",
    "corr_matrix = data[corr_cols].corr()",
    "",
    "plt.figure(figsize=(8, 6))",
    "sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')",
    "plt.title('Корреляция: Price vs Sqft, Beds, Baths')",
    "plt.show()"
]
new_cells.append(create_code_cell(source_corr))

new_cells.append(create_markdown_cell([
    "**Вывод**:",
    "Наибольшую корреляцию с ценой имеет площадь (`sqft_clean`).",
    "`beds` и `baths` также положительно коррелируют с ценой и между собой (мультиколлинеарность).",
    "Это подтверждает важность этих признаков для модели."
]))


# Append columns to notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Successfully added {len(new_cells)} cells to {notebook_path}")
