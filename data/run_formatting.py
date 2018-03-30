from glob import iglob
from pathlib import Path

import json

import pandas as pd

from formatting import add_HRG_Subchapter, remove_extra_columns, \
                       format_period_cols, format_dates, rename_columns

with open('./dtype_dict.json', 'r') as f:
    dtype_dict = json.load(f)

for csv_file in iglob('/Users/henrywilde/thesis-data/*.csv'):
    path = Path(csv_file)
    name = path.parts[-1]

    df = pd.read_csv(path, dtype=dtype_dict, low_memory=False)

    add_HRG_Subchapter(df)
    remove_extra_columns(df)
    format_period_cols(df)
    format_dates(df)
    rename_columns(df)

    df.to_csv(f'/Users/henrywilde/thesis-data/formatted/{name}',
              header=True, index=False)

print('Done!')
