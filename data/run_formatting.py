""" Full run of formatting. """

from glob import iglob
from pathlib import Path

import json

import pandas as pd

from formatting import add_HRG_Subchapter, remove_extra_columns, \
                       format_period_cols, format_dates, \
                       true_length_of_stay, rename_columns

def main_formatting(df):

    add_HRG_Subchapter(df)
    remove_extra_columns(df)
    format_period_cols(df)
    format_dates(df)
    true_length_of_stay(df)
    rename_columns(df)

    return df

with open('./dtype_dict.json', 'r') as f:
    dtypes = json.load(f)

for datafile in iglob('/Volumes/thesis-data/unformatted/*'):

    path = Path(datafile)
    name = path.parts[-1]
    new_name = name.replace('xlsx', 'csv')

    if name.endswith('xlsx'):
        df = pd.read_excel(path, dtype=dtypes)
    else:
        df = pd.read_csv(path, dtype=dtypes)

    print('Read:', name)

    df = main_formatting(df)
    df.to_csv(f'/Volumes/thesis-data/formatted/{new_name}',
              header=True, index=False)

    print('Done:', name, '\n')
