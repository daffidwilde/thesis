""" Create the data and plot the figure for the circle scenario. """

import edo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from edo.distributions import Uniform
from scipy.stats import gaussian_kde


class RadiusUniform(Uniform):

    name = "RadiusUniform"
    param_limits = {"bounds": [0, 2]}


class AngleUniform(Uniform):

    name = "AngleUniform"
    param_limits = {"bounds": [-2 * np.pi, 2 * np.pi]}


def split_individual(individual):
    """ Separate the columns of an individual's dataframe. """

    df, metadata = individual
    names = [m.name for m in metadata]
    radii = df[names.index("RadiusUniform")]
    angles = df[names.index("AngleUniform")]

    return radii, angles


def fitness(individual):
    """ Determine the similarity of the dataset to the unit circle. """

    radii, angles = split_individual(individual)
    return angles.var() / (radii - 1).abs().max()


def run():
    """Run the EDO algorithm."""

    pop_histories, fit_histories = [], []
    for seed in range(5):

        families = [edo.Family(RadiusUniform), edo.Family(AngleUniform)]

        opt = edo.DataOptimiser(
            fitness,
            size=100,
            row_limits=[50, 100],
            col_limits=[(1, 1), (1, 1)],
            families=families,
            max_iter=30,
            best_prop=0.1,
            maximise=True,
        )

        pops, fits = opt.run(random_state=seed)

        fits["seed"] = seed
        pop_histories.append(pops)
        fit_histories.append(fits)

    return pop_histories, pd.concat(fit_histories)


def get_contour(pop_histories, fit_history, low, upp):
    """Get the 3D grid for the contour plot."""

    xs_list, ys_list = [], []
    for seed, history in enumerate(pop_histories):
        fit = fit_history[fit_history["seed"] == seed]
        upper_quantile = fit["fitness"].quantile(0.5)
        acceptable = fit[fit["fitness"] > upper_quantile][
            ["generation", "individual"]
        ]
        for _, (gen, ind) in acceptable.iterrows():

            individual = history[gen][ind]
            radii, angles = split_individual(individual)
            xs, ys = radii * np.cos(angles), radii * np.sin(angles)

            xs_list.extend(list(xs))
            ys_list.extend(list(ys))

    xmin, xmax = ymin, ymax = low, upp

    xs, ys = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xs.ravel(), ys.ravel()])

    values = np.vstack([xs_list, ys_list])
    kernel = gaussian_kde(values)

    zs = np.reshape(kernel(positions).T, xs.shape)

    return xs, ys, zs


def make_plot(pop_histories, fit_history, xs, ys, zs, low, upp):
    """Plot the contour and scatter the best individual."""

    _, ax = plt.subplots(dpi=300)

    ax.contourf(xs, ys, zs, cmap="viridis_r")

    best_idx = fit_history["fitness"].idxmax()
    seed, gen, ind = fit_history[["seed", "generation", "individual"]].iloc[
        best_idx, :
    ]
    best = pop_histories[seed][gen][ind]

    radii, angles = split_individual(best)
    best_xs, best_ys = radii * np.cos(angles), radii * np.sin(angles)

    ax.scatter(best_xs, best_ys, color="white", marker=".")

    circle = plt.Circle((0, 0), 1, fill=False, linestyle="--", color="tab:gray")
    ax.add_artist(circle)

    ax.set(
        xlim=(low, upp),
        ylim=(low, upp),
        aspect="equal",
    )
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("main.pdf", transparent=True)


def main():
    """The main script."""

    print("Running EDO...")
    low, upp = -1.5, 1.5
    pop_histories, fit_history = run()
    print("Getting contour...")
    xs, ys, zs = get_contour(pop_histories, fit_history, low, upp)
    print("Making plot...")
    make_plot(pop_histories, fit_history, xs, ys, zs, low, upp)


if __name__ == "__main__":
    main()
