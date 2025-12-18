import pandas as pd

# Load data (only necessary columns to save memory)
try:
    data = pd.read_csv('/home/pavel/IDE/project_final_01/data/data.csv.zip', usecols=['homeFacts', 'schools'])
except:
    data = pd.read_csv('/home/pavel/IDE/project_final_01/data/data.csv', usecols=['homeFacts', 'schools'])

print("--- homeFacts sample ---")
for val in data['homeFacts'].dropna().head(3):
    print(val)
    print("-" * 20)

print("\n--- schools sample ---")
for val in data['schools'].dropna().head(3):
    print(val)
    print("-" * 20)
