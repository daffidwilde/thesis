import pandas as pd
import glob

dfs = []
for csv_path in glob.iglob('/Volumes/thesis-data/*.csv'):
    dfs.append(pd.read_csv(csv_path, low_memory=False))

pd.concat(dfs).to_csv('/Volumes/thesis-data/main.csv')
