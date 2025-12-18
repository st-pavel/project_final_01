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

# Header
new_cells.append(create_markdown_cell(["## 1.7. Анализ сложных признаков (homeFacts и schools)"]))

# Parsing Logic code
source_parsing = [
    "# Парсинг сложных колонок 'homeFacts' и 'schools'",
    "import ast",
    "import re",
    "",
    "# 1. Парсинг homeFacts",
    "def parse_homeFacts(val):",
    "    if pd.isna(val): return {}",
    "    try:",
    "        # Строка выглядит как словарь Python",
    "        d = ast.literal_eval(val)",
    "        facts = d.get('atAGlanceFacts', [])",
    "        result = {}",
    "        for fact in facts:",
    "            label = fact.get('factLabel', '')",
    "            value = fact.get('factValue', '')",
    "            if label and value:",
    "                result[label] = value",
    "        return result",
    "    except:",
    "        return {}",
    "",
    "# 2. Парсинг schools",
    "def parse_schools(val):",
    "    if pd.isna(val): return {'avg_rating': None, 'min_dist': None}",
    "    try:",
    "        # Строка выглядит как список с одним словарем",
    "        l = ast.literal_eval(val)",
    "        if not l or not isinstance(l, list): return {'avg_rating': None, 'min_dist': None}",
    "        d = l[0]",
    "        ",
    "        ratings = d.get('rating', [])",
    "        distances = d.get('data', {}).get('Distance', [])",
    "        ",
    "        # Обработка рейтингов",
    "        valid_ratings = []",
    "        for r in ratings:",
    "            try:",
    "                # Рейтинги могут быть 'NR', 'NA' или числами",
    "                if r and r not in ['NR', 'NA', 'None', '']:",
    "                    # Иногда рейтинг 'X/10', берем первую часть",
    "                    r_clean = r.split('/')[0]",
    "                    valid_ratings.append(float(r_clean))",
    "            except:",
    "                pass",
    "        ",
    "        avg_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else None",
    "        ",
    "        # Обработка дистанций",
    "        valid_dists = []",
    "        for dist in distances:",
    "            try:",
    "                # Дистанция '2.7 mi'",
    "                if dist:",
    "                    d_clean = re.findall(r\"\\d+\\.?\\d*\", dist)",
    "                    if d_clean:",
    "                        valid_dists.append(float(d_clean[0]))",
    "            except:",
    "                pass",
    "                ",
    "        min_dist = min(valid_dists) if valid_dists else None",
    "        ",
    "        return {'schools_avg_rating': avg_rating, 'schools_min_dist': min_dist}",
    "    except:",
    "        return {'schools_avg_rating': None, 'schools_min_dist': None}",
    "",
    "print(\"Функции парсинга определены.\")"
]
new_cells.append(create_code_cell(source_parsing))

# Apply parsing (Running on CPU/Pandas because of apply + ast)
source_apply = [
    "# Применяем парсинг. NB: Это медленная операция, так как выполняется на CPU с помощью apply.",
    "# Для ускорения можно использовать multiprocessing, но в ноутбуке это сложнее.",
    "print(\"Начинаем извлечение признаков... Это может занять время.\")",
    "",
    "# Работаем с копией в pandas для безопасности и совместимости",
    "try:",
    "    df_pandas = data.to_pandas()",
    "except:",
    "    df_pandas = data # Уже pandas",
    "",
    "# --- Extract homeFacts ---",
    "# Извлечем нужные поля: Year built, Remodeled year, Heating, Cooling, Parking, lotsize",
    "# Сначала применим парсинг ко всему столбцу",
    "home_facts_parsed = df_pandas['homeFacts'].apply(parse_homeFacts)",
    "",
    "# Создаем DataFrame из списка словарей",
    "home_facts_df = pd.json_normalize(home_facts_parsed)",
    "",
    "# Выбираем и переименовываем интересные колонки",
    "cols_of_interest = {",
    "    'Year built': 'year_built',",
    "    'Remodeled year': 'remodeled_year',",
    "    'Heating': 'heating',",
    "    'Cooling': 'cooling',",
    "    'Parking': 'parking',",
    "    'lotsize': 'lotsize_raw'",
    "}",
    "# Берем только существующие колонки",
    "available_cols = [c for c in cols_of_interest.keys() if c in home_facts_df.columns]",
    "home_facts_df = home_facts_df[available_cols].rename(columns=cols_of_interest)",
    "",
    "# --- Extract schools ---",
    "schools_parsed = df_pandas['schools'].apply(parse_schools)",
    "schools_df = pd.json_normalize(schools_parsed)",
    "",
    "# Объединяем с основным датафреймом",
    "df_pandas = pd.concat([df_pandas, home_facts_df, schools_df], axis=1)",
    "",
    "print(\"Извлечение завершено. Новые колонки:\", home_facts_df.columns.tolist() + schools_df.columns.tolist())",
    "",
    "# Конвертация 'year_built' в число",
    "df_pandas['year_built'] = pd.to_numeric(df_pandas['year_built'], errors='coerce')",
    "",
    "# Возвращаем в main data переменную (если используем cudf, конвертируем обратно)",
    "if USE_GPU:",
    "    import cudf",
    "    # cudf может не поддерживать object колонки со сложными типами, поэтому будьте осторожны",
    "    # data = cudf.DataFrame(df_pandas) # Это может быть тяжело по памяти",
    "    # Лучше пока оставим в pandas для EDA этих колонок или обновим только нужные",
    "    pass",
    "else:",
    "    data = df_pandas",
    "",
    "# Посмотрим на корреляцию новых числовых признаков с таргетом",
    "new_numeric_cols = ['year_built', 'schools_avg_rating', 'schools_min_dist', 'target']",
    "corr_new = df_pandas[new_numeric_cols].corr()",
    "",
    "plt.figure(figsize=(8, 6))",
    "sns.heatmap(corr_new, annot=True, cmap='coolwarm', fmt='.2f')",
    "plt.title('Корреляция новых признаков с Ценой')",
    "plt.show()"
]
new_cells.append(create_code_cell(source_apply))

# Append to notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Successfully added {len(new_cells)} cells to {notebook_path}")
