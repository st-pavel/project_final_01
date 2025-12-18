import json
import numpy as np

notebook_path = '/home/pavel/IDE/project_final_01/project_final_000.ipynb'

def create_code_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source_lines]
    }

source_fix = [
    "# FIX: Создание недостающих колонок для совместимости со старым кодом",
    "print(\"Восстановление колонок 'target_clean' и 'target_clean_log'...\")",
    "",
    "try:",
    "    # Убедимся, что target числовой",
    "    data['target'] = pd.to_numeric(data['target'], errors='coerce')",
    "    ",
    "    # Восстанавливаем target_clean как копию target",
    "    if 'target_clean' not in data.columns:",
    "        data['target_clean'] = data['target']",
    "        print(\"Колонка 'target_clean' создана.\")",
    "    ",
    "    # Восстанавливаем target_clean_log",
    "    if 'target_clean_log' not in data.columns:",
    "        # Используем numpy (работает и с pandas и с cudf, если импортирован как np)",
    "        # Добавим обработку нулей/отрицательных, если есть (хотя цена > 0)",
    "        data['target_clean_log'] = np.log(data['target_clean'])",
    "        print(\"Колонка 'target_clean_log' создана.\")",
    "        ",
    "    print(\"Готово. Теперь можно запускать ячейки, использующие эти колонки.\")",
    "    ",
    "except Exception as e:",
    "    print(f\"Ошибка при восстановлении колонок: {e}\")"
]

# Append to notebook
try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # Insert this cell at the beginning of the EDA section? 
    # Or just append it. Appending is safer to avoid messing up index too much, 
    # but user needs to run it.
    # Given the user is likely at the bottom or middle, appending is fine.
    
    nb['cells'].append(create_code_cell(source_fix))

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"Successfully added fix cell to {notebook_path}")

except Exception as e:
    print(f"Failed to update notebook: {e}")
