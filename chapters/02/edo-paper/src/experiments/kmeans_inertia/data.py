""" Functions for running trials for k-means with inertia and lower bounds. """

import sys
from pathlib import Path

from sklearn.cluster import KMeans

from edo_exp import run_trial

PATH = Path("../../../data/kmeans_inertia/")

NUM_CORES = int(sys.argv[1])
SIZE = int(sys.argv[2])
SELECTION = float(sys.argv[3])
MUTATION = float(sys.argv[4])
SEED = int(sys.argv[5])


def kmeans_fitness(dataframe, n_clusters=2, seed=0):
    """ Cluster the data into two parts and return the final inertia. """

    km = KMeans(n_clusters=n_clusters, random_state=seed)
    km.fit(dataframe)

    return km.inertia_


def main(num_cores, size, selection, mutation, seed):
    """ Run a trial and write the datasets to file. """

    root = PATH / str(seed)
    root.mkdir(exist_ok=True, parents=True)

    data = root / "data"
    data.mkdir(exist_ok=True)

    row_limits = [3, 100]
    col_limits = [2, 2]

    run_trial(
        data, kmeans_fitness, num_cores, size, row_limits, col_limits,
        selection, mutation, seed, {"seed": seed}
    )


if __name__ == "__main__":
    main(NUM_CORES, SIZE, SELECTION, MUTATION, SEED)
