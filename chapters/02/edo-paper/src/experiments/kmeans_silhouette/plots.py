""" Code to generate the plots for k-means with silhouette and lower bounds. """

from pathlib import Path
import sys
import warnings

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


SEED = 0
if len(sys.argv) == 2:
    SEED = int(sys.argv[1])

IMAGES = Path("../../../img/")
SUMMARY_DIR = Path(f"../../../data/kmeans_silhouette/{SEED}/summary/")
SUMMARY = pd.read_csv(SUMMARY_DIR / "main.csv")

plt.style.use("seaborn-colorblind")
warnings.filterwarnings("ignore")


def fitness_boxplot():
    """ Create a boxplot of the fitness progression. """

    _, ax = plt.subplots(figsize=(10, 3.5), dpi=300)

    data = -SUMMARY["fitness"].values.reshape((1001, 100))
    desired = range(0, 1001, 100)

    flierprops = dict(marker=".", markersize=2.5, linestyle="none")

    ax.boxplot(data[desired].T, flierprops=flierprops)

    ax.set_xticklabels(desired)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Silhouette score")

    plt.tight_layout()
    plt.savefig(IMAGES / "Fig9a-1.pdf", transparent=True)


def nrows_boxplot():
    """ Create a boxplot of the dimension progression. """

    _, ax = plt.subplots(figsize=(10, 3.5), dpi=300)

    data = SUMMARY["nrows"].values.reshape((1001, 100))
    desired = range(0, 51, 2)

    flierprops = dict(marker=".", markersize=2.5, linestyle="none")

    ax.boxplot(data[desired].T, flierprops=flierprops)

    ax.set_xticklabels(desired)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Number of rows")

    plt.tight_layout()
    plt.savefig(IMAGES / "Fig9a-2.pdf", transparent=True)


def kmeans_scatterplot():
    """ Create a scatter plot of the best, median and worst individuals found in
    the trial showing the clustering found. """

    order = ["best", "median", "worst"]

    _, axes = plt.subplots(ncols=3, figsize=(15, 5), dpi=300)

    for i, case in enumerate(("min", "median", "max")):

        dataframe = pd.read_csv(SUMMARY_DIR / f"{case}/main.csv")
        km = KMeans(n_clusters=2, random_state=SEED).fit(dataframe)

        axes[i].scatter(
            dataframe["0"], dataframe["1"], c=km.labels_, edgecolors="k", lw=0.5
        )
        axes[i].scatter(
            km.cluster_centers_[:, 0],
            km.cluster_centers_[:, 1],
            s=50,
            marker="X",
            c=[0, 1],
            edgecolors="k",
            lw=0.5,
        )
        axes[i].set_title(
            order[i].title() + f"    (Inertia: {km.inertia_:.4e})"
        )

    plt.tight_layout()
    plt.savefig(IMAGES / f"Fig10a.pdf", transparent=True)


if __name__ == "__main__":
    fitness_boxplot()
    nrows_boxplot()
    kmeans_scatterplot()
