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

# 1. Stats Header
new_cells.append(create_markdown_cell(["## 1.6. Статистические тесты (Hypothesis Testing)"]))

# 2. Kruskal-Wallis Test
source_stats = [
    "# Проверка гипотезы: Зависит ли стоимость недвижимости (target) от количества спален (beds)?",
    "# Используем критерий Краскела-Уоллиса, так как распределение цены, скорее всего, ненормальное.",
    "",
    "from scipy import stats",
    "",
    "try:",
    "    unique_beds = sorted(data['beds'].unique().to_numpy())",
    "except:",
    "    unique_beds = sorted(data['beds'].unique()) # Если pandas",
    "",
    "beds_groups = []",
    "labels = []",
    "",
    "for b in unique_beds:",
    "    # Выбираем цены для каждого количества спален",
    "    group = data[data['beds'] == b]['target'].dropna()",
    "    try:",
    "        group = group.to_numpy()",
    "    except:",
    "        pass",
    "    ",
    "    # Берем группы, где хотя бы 50 записей, для надежности",
    "    if len(group) > 50:",
    "        beds_groups.append(group)",
    "        labels.append(b)",
    "",
    "if len(beds_groups) > 1:",
    "    stat, p_value = stats.kruskal(*beds_groups)",
    "    print(f\"Kruskal-Wallis для зависимости Цены от Спален (beds): Statistic={stat:.2f}, p-value={p_value:.4e}\")",
    "",
    "    alpha = 0.05",
    "    if p_value < alpha:",
    "        print(\"Результат: Отвергаем H0. Существует статистически значимая разница в стоимости квартир с разным количеством спален.\")",
    "    else:",
    "        print(\"Результат: Не отвергаем H0. Разница не статистически значима.\")",
    "else:",
    "    print(\"Недостаточно групп для проведения теста.\")"
]
new_cells.append(create_code_cell(source_stats))


# Append to notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

nb['cells'].extend(new_cells)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Successfully added {len(new_cells)} cells to {notebook_path}")
