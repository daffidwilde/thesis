import os

from seaborn import color_palette
from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


blue = color_palette("colorblind")[0]

costs = [
    "COST",
    "NetCost",
    "DRUG",
    "ENDO",
    "HCD",
    "EMER",
    "CRIT",
    "IMG",
    "IMG_OTH",
    "MED",
    "NCI",
    "NID",
    "OCLST",
    "OPTH",
    "OTH",
    "OTH_OTH",
    "OUTP",
    "OVH",
    "PATH",
    "PATH_OTH",
    "PHAR",
    "PROS",
    "RADTH",
    "SECC",
    "SPS",
    "THER",
    "WARD",
]

components = costs[2:]


def get_contribution_variation(df):
    """
    Return a dataframe containing the mean contribution to the net cost of our
    cost components, and their respective coefficients of variation.
    """
    summed_costs = df.groupby("SPELL_ID")[costs].sum()
    variations = summed_costs.std() / summed_costs.mean()
    netcost = summed_costs["NetCost"]
    contributions = summed_costs[components].divide(netcost, axis=0).mean()

    corr = summed_costs.corr()
    order = sorted(corr.columns, key=lambda col: abs(corr[col]).sum())[::-1]

    cont_var = pd.concat(
        [contributions, variations[components]], axis=1
    ).rename({0: "contribution", 1: "variation"}, axis=1)

    return cont_var.reindex(order).dropna()


def make_size_legend(ax):
    """
    Make legend for scatter size.
    """
    sizes = [2, 5, 10, 25, 40]
    for i, size in enumerate(sizes):
        ax.scatter(
            [],
            [],
            marker=".",
            s=size * 1e3,
            alpha=0.75,
            facecolor=blue,
            edgecolor="None",
            label=size,
        )

    handles, labels = ax.get_legend_handles_labels()
    title = "Coefficient of" + "\n" + r"variation ($C_v$)"

    legend = ax.legend(
        handles,
        labels,
        loc="best",
        labelspacing=3,
        fontsize=30,
        handletextpad=3,
        edgecolor="None",
        facecolor="None",
        title=title,
    )

    legend.get_title().set_fontsize(30)
    legend._legend_box.sep = 60
    ax.set_xlim(0, 0.04)
    ax.axis("off")

    return legend


def plot_cost_bubble(df):
    """
    'Bubble' plot to illustrate the relative importance of our cost components.
    Effectively, a scatter plot of the average contribution to net cost of a
    spell for each component where the size of the marker is proportional to the
    corresponding coefficient of variation.
    """
    fontsize = 30
    cont_var = get_contribution_variation(df)

    fig, (ax, size_ax) = plt.subplots(
        ncols=2,
        figsize=(24, 12),
        dpi=400,
        gridspec_kw={"width_ratios": [16, 1]},
    )

    for point in cont_var.iterrows():
        variation = abs(point[1]["variation"])
        ax.scatter(
            point[0],
            point[1]["contribution"],
            s=1e3 * variation,
            marker=".",
            zorder=2.5 - (0.01 * variation),
            alpha=0.75,
            edgecolor="None",
            facecolor=blue,
        )
        ax.scatter(
            point[0],
            point[1]["contribution"],
            s=100,
            marker=".",
            zorder=2.5 - (0.01 * variation),
            color="w",
        )
        ax.vlines(point[0], -1, point[1]["contribution"], "grey", "dotted")

    size_legend = make_size_legend(size_ax)

    ax.set_ylabel("Average proportion of net cost", fontsize=fontsize)
    ax.set_ylim(-0.1, 0.3)

    ax.set_axisbelow(True)
    ax.grid(b=True, which="major", axis="y")
    ax.set_yticks(ax.get_yticks()[1:-1])

    ax.set_xlim(ax.get_xlim())
    ax.hlines(0, *ax.get_xlim(), color='r', lw=2)

    for label in ax.get_yticklabels():
        label.set_fontsize(fontsize)

    for label in ax.get_xticklabels():
        label.set_fontsize(fontsize)
        label.set_rotation(45)
        label.set_horizontalalignment("right")

    plt.tight_layout()

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.savefig(filename, transparent=True)
