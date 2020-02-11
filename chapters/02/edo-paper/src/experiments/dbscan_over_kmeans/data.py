""" Functions for running trials where DBSCAN is preferred over k-means. """

import sys
from pathlib import Path

import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import silhouette_score

from edo_exp import run_trial

PATH = Path("../../../data/dbscan_over_kmeans/")

NUM_CORES = int(sys.argv[1])

SIZE = int(sys.argv[2])
SELECTION = float(sys.argv[3])
MUTATION = float(sys.argv[4])
SEED = int(sys.argv[5])


def difference_fitness(
    dataframe, n_clusters=3, eps=0.1, min_samples=5, seed=0
):
    """ Cluster the data into three parts with k-means, and with DBSCAN. Return
    the difference between their silhouette scores so as to maximise that of
    DBSCAN. If no valid silhouette can be found for the DBSCAN clustering,
    return a penalty of infinity. """

    km = KMeans(n_clusters=n_clusters, random_state=seed).fit(dataframe)
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(dataframe)

    if len(set(db.labels_)) > 1:
        km_silhouette = silhouette_score(dataframe, km.labels_)
        db_silhouette = silhouette_score(dataframe, db.labels_)

        return km_silhouette - db_silhouette # EDO minimises by default

    return np.infty


def main(num_cores, size, selection, mutation, seed):
    """ Run a trial and write the datasets to file using the given parameters.
    """

    root = PATH / str(seed)
    root.mkdir(exist_ok=True, parents=True)

    data = root / "data"
    data.mkdir(exist_ok=True)

    row_limits = [50, 100]
    col_limits = [2, 2]

    run_trial(
        data, difference_fitness, num_cores, size, row_limits, col_limits,
        selection, mutation, seed, {"seed": seed}
    )


if __name__ == "__main__":
    main(NUM_CORES, SIZE, SELECTION, MUTATION, SEED)
