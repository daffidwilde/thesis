""" The worker function. """

import time

import numpy as np
from dask import delayed

from sampling import concat_dataframes, get_sample


@delayed
def write_dataframes(root, X, Y, beta, size, seed, sample_idx):
    """ Write to file the resulting partition dataframes from locating and
    collecting similar pairs between two sets and for a given run.

    Parameters
    ----------
    root : str
        Root directory to write results to.
    X, Y : dataframe
        Dask dataframes to take samples from
    sample_idx : int
        Sample identifier
    seed : int
        Pseudo-random number generator seed
    beta : float
        Quality measure for similarity of pairs
    size : int
        Size of sample to be taken
    """

    start = time.clock()

    # Take a sample from each set
    x_sample = get_sample(X, seed, size)
    y_sample = get_sample(Y, seed, size)

    # Drop irrelevant columns
    irrelevant_columns = ["animal_name", "class_type", "catsize"]
    x_sample.drop(irrelevant_columns, axis=1)
    y_sample.drop(irrelevant_columns, axis=1)

    dataframe = concat_dataframes(x_sample, y_sample, sample_idx, seed, beta, size)

    time_taken = time.clock() - start

    if np.any(dataframe):

        dataframe["time"] = time_taken
        dataframe.to_csv(f"{root}/{beta}/{size}/{seed}/{sample_idx}/", index=False)
