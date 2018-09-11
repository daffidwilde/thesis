import json
import pandas as pd

# Load in the data
with open("/Volumes/thesis-data/dtype_dict.json") as f:
    dtypes = json.load(f)

df = pd.read_csv(
    "/Volumes/thesis-data/main.csv",
    dtype=dtypes,
    parse_dates=["PERIOD", "ADMDATE", "DISCDATE"],
)
