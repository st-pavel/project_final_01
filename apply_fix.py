import json

notebook_path = '/home/pavel/IDE/project_final_01/project_final_000.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The code provided by the user
new_source = [
    "# Принудительно конвертируем в числа, ошибки (текст) превращаем в NaN\n",
    "cols = ['target', 'sqft', 'beds', 'baths']\n",
    "for col in cols:\n",
    "    data[col] = pd.to_numeric(data[col], errors='coerce')\n",
    "\n",
    "# Теперь считаем корреляцию\n",
    "corr_matrix = data[cols].corr()\n",
    "\n",
    "\n",
    "# 1. Принудительно выгружаем данные в NumPy (на процессор)\n",
    "# Это работает, потому что .to_numpy() — стандартный метод Pandas\n",
    "corr_array = corr_matrix.to_numpy()\n",
    "\n",
    "plt.figure(figsize=(8, 6))\n",
    "\n",
    "# 2. Передаем массив в Seaborn, но подписываем оси вручную\n",
    "# (так как массив потерял названия колонок)\n",
    "sns.heatmap(\n",
    "    corr_array, \n",
    "    xticklabels=corr_matrix.columns,\n",
    "    yticklabels=corr_matrix.index,\n",
    "    annot=True, \n",
    "    cmap='coolwarm', \n",
    "    fmt='.2f'\n",
    ")\n",
    "\n",
    "plt.title('Корреляция числовых признаков')\n",
    "plt.show()"
]

# Find the last cell (which caused the error) and update it
# We look for the cell that calculates correlation
found = False
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source_str = "".join(cell['source'])
        if "corr_matrix = data[['target', 'sqft', 'beds', 'baths']].corr()" in source_str:
            cell['source'] = new_source
            found = True
            break

if found:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Notebook cell updated successfully.")
else:
    print("Target cell not found.")
