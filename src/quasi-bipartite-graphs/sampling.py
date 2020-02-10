"""
Script for the collection and manipulation of similar pairs of points in a given
dataset, using Dask to parallelise the process of finding these pairs.
"""

import dask.dataframe as dd
import numpy as np
import pandas as pd
from dask import delayed


def dissim(Y, x):
    """ Return normalised pointwise dissimilarity between a point x and all
    points in the set Y. """

    return np.sum(Y != x, axis=1) / len(x)


def get_sample(X, seed, size):
    """ Take a random sample of `size` rows from a dataframe object, specified
    by a random number generator `seed`. """

    frac = size / len(X)
    sample = X.sample(frac, random_state=seed)

    return sample


@delayed
def build_matrices(X, Y, beta, size):
    """ Return two matrices: a dissimilarity and an adjacency matrix. The latter
    is formed from the first, and they are defined as follows:

    dissim_matrix[i, j] = dissim(X[i], Y[j])

    adjacency_matrix[i, j] = {1 if dissim_matrix[i, j] <= beta;
                             {0, otherwise

    Parameters
    ----------
    X, Y : dataframe
        Sample dask dataframes to find similar pairs in
    beta : float
        A measure of the quality of the pairs to be found
    size : int
        The size of both X and Y (sample size)

    Returns
    -------
    adjacency_matrix : array, shape=[size, size]
        Indicator matrix indicating whether two points are sufficiently similar
        based on the value of `beta`
    dissim_matrix : array, shape=[size, size]
        Dissimilarity matrix. Each row is the dissimilarity of Y with X[i]
    """

    x_arr = X.values.compute()
    y_arr = Y.values.compute()

    dissim_matrix = np.empty((size, size))

    for i, x_row in enumerate(x_arr):
        dissim_matrix[i, :] = dissim(y_arr, x_row)

    adjacency_matrix = np.where(dissim_matrix <= beta, 1, 0)

    return adjacency_matrix, dissim_matrix


@delayed
def build_dataframe(
    X, Y, adjacency_matrix, dissim_matrix, idxs, sample_idx, seed, beta, size
):
    """ Return a dataframe object for a pair of points given by idxs. """

    x_idx = X.index.compute()[idxs[0]]
    y_idx = Y.index.compute()[idxs[1]]

    result_df = pd.DataFrame(
        {
            "sample_idx": sample_idx,
            "seed": seed,
            "beta": beta,
            "dissim": dissim_matrix[idxs[0], idxs[1]],
            f"{X}_idx": x_idx,
            f"{Y}_idx": y_idx,
            "sample_size": size,
        },
        index=[""],
    )

    return result_df


def concat_dataframes(X, Y, sample_idx, seed, beta, size):
    """ Return a dask dataframe detailing all the similar pairs found between
    the two sets, X and Y, and the details of this run.

    Parameters
    ----------
    X, Y : dask.dataframe
        Dask dataframe samples
    sample_idx : int
        Identifier for sample run
    seed : int
        Random number seed
    beta : float
        Quality measure of similar points in this particular run
    size : int
        Sample size taken in this run

    Returns
    -------
    dataframe : dataframe
        Result dataframe
    """

    adjacency_matrix, dissim_matrix = build_matrices(X, Y, beta, size)

    row_idxs, col_idxs = np.where(adjacency_matrix == 1)
    idx_pairs = zip(row_idxs, col_idxs)

    dfs = []
    for idxs in idx_pairs:
        result_df = build_dataframe(
            X,
            Y,
            adjacency_matrix,
            dissim_matrix,
            idxs,
            sample_idx,
            seed,
            beta,
            size,
        )
        dfs.append(result_df)

    if dfs:
        dataframe = dd.concat(dfs, axis=0, interleave_partitions=True)

        return dataframe
