""" Full run of formatting. """

import json
import sys
from glob import iglob
from pathlib import Path

import pandas as pd

from formatting import (
    add_HRG_Subchapter,
    drop_true_los_rows,
    format_dates,
    format_period_cols,
    remove_extra_columns,
    rename_columns,
    true_length_of_stay,
)

if __name__ == "__main__":

    if len(sys.argv) == 1:
        root = "unformatted"
    else:
        root = str(sys.argv[1])


def main_formatting(df):

    add_HRG_Subchapter(df)
    remove_extra_columns(df)
    format_period_cols(df)
    format_dates(df)
    true_length_of_stay(df)
    rename_columns(df)
    df = drop_true_los_rows(df)

    return df


with open("./dtype_dict.json", "r") as f:
    dtypes = json.load(f)

for datafile in iglob(f"/Volumes/thesis-data/{root}/*"):

    path = Path(datafile)
    name = path.parts[-1]
    new_name = name.replace(".xlsx", ".csv")

    print("Start:", name)

    if name.endswith("xlsx"):
        df = pd.read_excel(path, dtype=dtypes)
    else:
        df = pd.read_csv(path, dtype=dtypes)

    print("Read:", name)

    df = main_formatting(df)
    df.to_csv(
        f"/Volumes/thesis-data/formatted/{new_name}", header=True, index=False
    )

    print("Done:", name, "\n")
