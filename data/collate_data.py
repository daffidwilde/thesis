from glob import iglob
import json
import pandas as pd

with open('dtype_dict.json', 'r') as f:
    dtypes = json.load(f)

csv_files = [csv for csv in iglob('/Volumes/thesis-data/formatted/*.csv')]
dfs = [pd.read_csv(csv, dtype=dtypes, low_memory=False) for csv in csv_files]

data = pd.concat(dfs, axis=0)
data.to_csv('/Volumes/thesis-data/main.csv', index=False)
