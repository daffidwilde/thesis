import dask.dataframe as dd
import glob

# Read in all the individual datasets

csvs = [csv for csv in glob.iglob('/Volumes/thesis-data/formatted/*.csv')]
dataframes = [dd.read_csv(csv, dtype={'OPCS_11': 'object', 'OPCS_12': 'object', 'ADM_MET': 'object'}, assume_missing=True, low_memory=False) for csv in csvs]

# Concatenate into one Dask DataFrame and write to "csv". 
# This is in fact a collection of .part files (one for each partition)
# Parallelised writing to csv is a difficult task so it is broken up into the partitions.

data = dd.concat(dataframes, axis=0)
data.to_csv('/Volumes/thesis-data/', index=False)

# Read in all .part files and write them to a single main.csv file

parts = glob.iglob('/Volumes/thesis-data/*.part')
with open('/Volumes/thesis-data/main.csv', 'w') as main:

    # We with to write the headers from the first file 
    # and skip them on all the subsequent .part files
    
    i = 0
    for part in parts:
        if i == 0:
            with open(part) as f:
                main.write(f.read())
            i += 1
        else:
            with open(part) as f:
                # Skip the first row (headers)
                next(f)
                main.write(f.read())


