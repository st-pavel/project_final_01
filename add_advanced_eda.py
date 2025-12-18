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

# 1. Feature Analysis - Header
new_cells.append(create_markdown_cell(["## 1.4. Анализ распределения признаков (Feature Distribution Analysis)"]))

# 2. Identify types cell
source_identify = [
    "# Определение числовых и категориальных признаков",
    "try:",
    "    numerical_cols = data.select_dtypes(include=['number']).columns.tolist()",
    "    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()",
    "except:",
    "    # Fallback if using pure cudf without same api metadata sometimes",
    "    numerical_cols = [c for c in data.columns if data[c].dtype != 'object']",
    "    categorical_cols = [c for c in data.columns if data[c].dtype == 'object']",
    "",
    "print(f\"Числовые признаки ({len(numerical_cols)}): {numerical_cols}\")",
    "print(f\"Категориальные признаки ({len(categorical_cols)}): {categorical_cols}\")"
]
new_cells.append(create_code_cell(source_identify))

# 3. Numerical Plots
source_num_plots = [
    "# Визуализация распределения числовых признаков",
    "# Используем .to_numpy() для совместимости с seaborn/matplotlib при работе на GPU",
    "",
    "for col in numerical_cols:",
    "    if col == 'target': continue # Уже анализировали",
    "    ",
    "    plt.figure(figsize=(12, 5))",
    "    ",
    "    # Гистограмма",
    "    plt.subplot(1, 2, 1)",
    "    # dropna() нужен, чтобы seaborn не ломался на NaN",
    "    valid_data = data[col].dropna().to_numpy()",
    "    sns.histplot(valid_data, kde=True, bins=30)",
    "    plt.title(f'Distribution of {col}')",
    "    ",
    "    # Boxplot",
    "    plt.subplot(1, 2, 2)",
    "    sns.boxplot(x=valid_data)",
    "    plt.title(f'Boxplot of {col}')",
    "    ",
    "    plt.tight_layout()",
    "    plt.show()"
]
new_cells.append(create_code_cell(source_num_plots))

# 4. Categorical Plots
source_cat_plots = [
    "# Анализ топ-10 значений для категориальных признаков",
    "for col in categorical_cols:",
    "    if col not in data.columns: continue",
    "    ",
    "    # Получаем топ-10 значений. ",
    "    # value_counts() работает в cudf, но для графика конвертируем в pandas",
    "    vc = data[col].value_counts().head(10)",
    "    ",
    "    try:",
    "        vc_pandas = vc.to_pandas()",
    "    except AttributeError:",
    "        vc_pandas = vc # Если мы уже на CPU",
    "        ",
    "    plt.figure(figsize=(10, 5))",
    "    sns.barplot(x=vc_pandas.values, y=vc_pandas.index)",
    "    plt.title(f'Top 10 occurrences in category: {col}')",
    "    plt.xlabel('Count')",
    "    plt.show()"
]
new_cells.append(create_code_cell(source_cat_plots))

# 5. Outliers Header
new_cells.append(create_markdown_cell(["## 1.5. Выявление и обработка выбросов (Outlier Handling)"]))

# 6. Outlier removal using IQR
source_outliers = [
    "def remove_outliers_iqr(df, column, multiplier=1.5):",
    "    # Вычисляем квантили",
    "    Q1 = df[column].quantile(0.25)",
    "    Q3 = df[column].quantile(0.75)",
    "    IQR = Q3 - Q1",
    "    ",
    "    lower_bound = Q1 - multiplier * IQR",
    "    upper_bound = Q3 + multiplier * IQR",
    "    ",
    "    print(f\"Column {column}: Removing outliers outside [{lower_bound:.2f}, {upper_bound:.2f}]\")",
    "    ",
    "    # Фильтрация",
    "    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]",
    "",
    "# Удаляем выбросы по цене (target) и площади (sqft), так как это ключевые факторы",
    "print(f\"Размер датасета до очистки выбросов: {data.shape}\")",
    "",
    "data_clean = remove_outliers_iqr(data, 'target')",
    "data_clean = remove_outliers_iqr(data_clean, 'sqft')",
    "",
    "print(f\"Размер датасета после очистки выбросов: {data_clean.shape}\")",
    "",
    "# Сравнение распределения цены до и после",
    "plt.figure(figsize=(12, 5))",
    "plt.subplot(1, 2, 1)",
    "sns.histplot(data['target'].to_numpy(), kde=True, color='red', alpha=0.3, label='Original')",
    "plt.title('Original Target Distribution')",
    "",
    "plt.subplot(1, 2, 2)",
    "sns.histplot(data_clean['target'].to_numpy(), kde=True, color='green', alpha=0.5, label='Cleaned')",
    "plt.title('Cleaned Target Distribution')",
    "plt.show()",
    "",
    "# Сохраняем очищенные данные в переменную data для дальнейшей работы",
    "# data = data_clean # Раскомментируйте, если готовы применить изменения глобально"
]
new_cells.append(create_code_cell(source_outliers))

# Write to notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Successfully added {len(new_cells)} cells to {notebook_path}")
