from glob import iglob
from pathlib import Path

import json

import pandas as pd

from formatting import add_HRG_Subchapter, remove_extra_columns, \
                       format_period_cols, format_dates, rename_columns


def main_formatting(df):

    add_HRG_Subchapter(df)
    remove_extra_columns(df)
    format_dates(df)
    rename_columns(df)

    return df

with open('./dtype_dict.json', 'r') as f:
    dtype_dict = json.load(f)

for excel_file in iglob('/Users/henrywilde/thesis-data/unformatted/*.xlsx'):
    path = Path(excel_file)
    name = path.parts[-1]
    new_name = name.replace('xlsx', 'csv')

    df = pd.read_excel(path, dtype=dtype_dict)
    df = main_formatting(df)
    df.to_csv(f'../../thesis-data/formatted/{new_name}',
              header=True, index=False)

    print('Done:', name)

for csv_file in iglob('/Users/henrywilde/thesis-data/unformatted/*.csv'):
    path = Path(csv_file)
    name = path.parts[-1]

    df = pd.read_csv(path, dtype=dtype_dict, low_memory=False)
    df = main_formatting(df)
    df.to_csv(f'/Users/henrywilde/thesis-data/formatted/{name}',
              header=True, index=False)

    print('Done:', name)
