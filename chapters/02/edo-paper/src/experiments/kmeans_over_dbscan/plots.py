""" Code to generate the plots for DBSCAN over k-means. """

from pathlib import Path
import sys
import warnings

import alphashape as alph
from alphashape.optimizealpha import _testalpha
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Patch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
import pandas as pd
import scipy
import shapely
from descartes import PolygonPatch
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import silhouette_score


SEED = 0
if len(sys.argv) == 2:
    SEED = int(sys.argv[1])

IMAGES = Path("../../../img/")
DATA_DIR = Path(f"../../../data/kmeans_over_dbscan/{SEED}/data/")
SUMMARY_DIR = Path(f"../../../data/kmeans_over_dbscan/{SEED}/summary/")
SUMMARY = pd.read_csv(SUMMARY_DIR / "main.csv")

plt.style.use("seaborn-colorblind")
warnings.filterwarnings("ignore")


def fitness_boxplot():
    """ Create a boxplot of the fitness progression. """

    _, ax = plt.subplots(figsize=(10, 3.5), dpi=300)

    data = SUMMARY["fitness"].values.reshape((1001, 100))
    desired = range(0, 1001, 100)

    flierprops = dict(marker=".", markersize=2.5, linestyle="none")

    ax.boxplot(data[desired].T, flierprops=flierprops)

    ax.set_xticklabels(desired)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Fitness")

    plt.tight_layout()
    plt.savefig(IMAGES / "Fig11-1.pdf", transparent=True)


def nrows_boxplot():
    """ Create a boxplot of the dimension progression. """

    _, ax = plt.subplots(figsize=(10, 3.5), dpi=300)

    data = SUMMARY["nrows"].values.reshape((1001, 100))
    desired = range(0, 1001, 100)

    flierprops = dict(marker=".", markersize=2.5, linestyle="none")

    ax.boxplot(data[desired].T, flierprops=flierprops)

    ax.set_xticklabels(desired)
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Number of rows")

    plt.tight_layout()
    plt.savefig(IMAGES / "Fig11-2.pdf", transparent=True)


def _optimise_alpha(points, max_iter=100, tol=1e-4, upper=1000):
    """ Bisection optimisation. """

    points = shapely.geometry.MultiPoint(points)
    lower = 0
    itr = 0
    while (upper - lower) > tol and itr < max_iter:

        itr += 1
        test = (upper + lower) / 2

        if _testalpha(points, test):
            lower = test
        else:
            upper = test

    return lower


def convexity_scatterplot_kmeans():
    """ Create a scatter for the best, median and worst individuals in the
    trial. Also illustrate the concave and convex hulls of the k-means
    clustering of those individuals. """

    order = ["best", "median", "worst"]

    _, axes = plt.subplots(ncols=3, figsize=(15, 5), dpi=300)

    for i, case in enumerate(("min", "median", "max")):

        dataframe = pd.read_csv(SUMMARY_DIR / f"{case}/main.csv")
        km = KMeans(n_clusters=3, random_state=SEED).fit(dataframe)
        score = silhouette_score(dataframe, km.labels_)

        scatter = axes[i].scatter(
            dataframe["0"],
            dataframe["1"],
            c=km.labels_,
            label=km.labels_,
            edgecolors="k",
            lw=0.5,
            zorder=2,
        )
        axes[i].set_title(
            order[i].title() + f"    ($k$-means silhouette: {score:.4f})"
        )

        measures = []
        patches = []
        for label in set(km.labels_):
            try:
                mask = km.labels_ == label
                X = dataframe.values[mask, :]
                convex = scipy.spatial.ConvexHull(X)
                for simplex in convex.simplices:
                    axes[i].plot(
                        X[simplex, 0], X[simplex, 1], "k-", lw=1, zorder=1
                    )

                alpha = _optimise_alpha(X)
                concave = alph.alphashape(X, alpha)
                convex = shapely.geometry.Polygon(X[convex.vertices, :])

                patches.append(PolygonPatch(concave))
                measures.append(f"{concave.area / convex.area:.3f}")

            except scipy.spatial.qhull.QhullError:
                measures.append("1.000")

        mean = np.array(measures, dtype=float).mean()

        collection = PatchCollection(patches, zorder=0, alpha=0.3)
        axes[i].add_collection(collection)

        handles, _ = scatter.legend_elements()
        axes[i].legend(
            handles + [Patch(facecolor="None", edgecolor="None")],
            measures + [f"Mean: {mean:.3f}"],
            title="Cluster convexity",
        )

    plt.tight_layout()
    plt.savefig(IMAGES / "Fig12a.pdf", transparent=True)


def convexity_scatterplot_dbscan():
    """ Create a scatter for the best, median and worst individuals in the
    trial. Also illustrate the concave and convex hulls of the DBSCAN
    clustering of those individuals. """

    order = ["best", "median", "worst"]

    _, axes = plt.subplots(ncols=3, figsize=(15, 5), dpi=300)

    for i, case in enumerate(("min", "median", "max")):

        dataframe = pd.read_csv(SUMMARY_DIR / f"{case}/main.csv")
        db = DBSCAN(eps=0.1, min_samples=5).fit(dataframe)
        try:
            score = silhouette_score(dataframe, db.labels_)
        except ValueError:
            score = np.nan

        outlier_mask = db.labels_ == -1
        X = dataframe.values[outlier_mask, :]
        axes[i].scatter(
            X[:, 0], X[:, 1], c="k", edgecolors="k", s=5, lw=0.5, zorder=2
        )

        X = dataframe.values[~outlier_mask, :]
        scatter = axes[i].scatter(
            X[:, 0],
            X[:, 1],
            c=db.labels_[~outlier_mask],
            label=db.labels_[~outlier_mask],
            edgecolors="k",
            lw=0.5,
            zorder=2,
        )
        axes[i].set_title(
            order[i].title() + f"    (DBSCAN silhouette: {score:.4f})"
        )

        measures = []
        patches = []
        for label in set(db.labels_):
            if label != -1:
                try:
                    mask = db.labels_ == label
                    X = dataframe.values[mask, :]
                    convex = scipy.spatial.ConvexHull(X)
                    for simplex in convex.simplices:
                        axes[i].plot(
                            X[simplex, 0], X[simplex, 1], "k-", lw=1, zorder=1
                        )

                    alpha = _optimise_alpha(X)
                    concave = alph.alphashape(X, alpha)

                    convex = shapely.geometry.Polygon(X[convex.vertices, :])
                    intersection = convex.intersection(concave)

                    patches.append(PolygonPatch(concave))
                    measures.append(f"{concave.area / convex.area:.3f}")

                except scipy.spatial.qhull.QhullError:
                    measures.append("1.000")

        mean = np.array(measures, dtype=float).mean()

        collection = plt.matplotlib.collections.PatchCollection(
            patches, zorder=0, alpha=0.3
        )
        axes[i].add_collection(collection)

        handles, _ = scatter.legend_elements()
        axes[i].legend(
            handles + [Patch(facecolor="None", edgecolor="None")],
            measures + [f"Mean: {mean:.3f}"],
            title="Cluster convexity",
        )

    plt.tight_layout()
    plt.savefig(IMAGES / "Fig12b.pdf", transparent=True)


def coverage_scatterplot():
    """ Create a scatter plot to demonstrate coverage of EDO. """

    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)

    cmap = plt.cm.viridis
    norm = plt.matplotlib.colors.Normalize(vmin=0, vmax=1000)

    for gen in range(0, 1001, 50):

        dfs = (
            pd.read_csv(DATA_DIR / f"{gen}/{ind}/main.csv")
            for ind in range(100)
        )
        df = pd.concat(dfs, axis=0, ignore_index=True)

        colour = cmap(norm(gen))
        ax.scatter(
            df["0"],
            df["1"],
            marker=".", zorder=gen, alpha=0.5, facecolor=colour,
            edgecolor="None",
        )

    ylims = ax.get_ylim()
    ax.set_ylim(ylims[0], ylims[1] + 0.1)

    cax = inset_axes(
        ax,
        width="80%",
        height="5%",
        loc='lower left',
        bbox_to_anchor=(0.1, 0.95, 1, 1),
        bbox_transform=ax.transAxes,
        borderpad=0,
    )

    fig.colorbar(
        plt.cm.ScalarMappable(cmap=cmap, norm=norm),
        ax=ax,
        cax=cax,
        orientation="horizontal",
    )

    ax.set_title("Generation")
    ax.set_aspect("equal")

    plt.tight_layout(rect=(0, 0, 1, 1))
    plt.savefig(
        IMAGES / "Fig15.pdf", transparent=True
    )


if __name__ == "__main__":
    fitness_boxplot()
    nrows_boxplot()
    convexity_scatterplot_dbscan()
    convexity_scatterplot_kmeans()
    try:
        coverage_scatterplot()
    except FileNotFoundError:
        pass
