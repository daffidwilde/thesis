import os
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sbn

sbn.set_palette("colorblind")
colours = cycle(sbn.color_palette())
blue = next(colours)
green = next(colours)

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
    np.random.seed(3)

    summed_costs = df.groupby("SPELL_ID")[costs].sum()
    variations = summed_costs.std() / summed_costs.mean()
    netcost = summed_costs["NetCost"]
    contributions = summed_costs[components].divide(netcost, axis=0).mean()

    cont_var = pd.concat([contributions, variations[components]], axis=1).rename(
        {0: "contribution", 1: "variation"}, axis=1
    )

    return cont_var


def make_legend(ax):
    """
    Make the legend for the main plot by scattering patches and grouping
    together in the legend.
    """
    diab_outer = ax.scatter(
        [], [], marker="o", s=100, alpha=0.75, edgecolor="None", facecolor=green
    )
    diab_inner = ax.scatter([], [], marker=".", s=10, color="w")
    nondiab_outer = ax.scatter(
        [], [], marker="o", s=100, alpha=0.75, edgecolor="None", facecolor=blue
    )
    nondiab_inner = ax.scatter(
        [], [], marker=".", s=10, edgecolor="None", facecolor=blue
    )

    patches = ((nondiab_outer, nondiab_inner), (diab_outer, diab_inner))
    legend = ax.legend(
        patches,
        (("non-diabetic"), ("diabetic")),
        loc="best",
        fontsize=20,
        markerscale=2.5,
    )
    legend.get_title().set_fontsize(20)

    return legend


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
    title = r"Coefficient of" + "\n" + "variation ($C_v$)"

    legend = ax.legend(
        handles,
        labels,
        loc="best",
        labelspacing=5.5,
        fontsize=20,
        handletextpad=4,
        edgecolor="None",
        title=title,
        facecolor="None",
    )

    legend.get_title().set_fontsize(24)
    legend._legend_box.sep = 60
    ax.set_xlim(0, 0.04)
    ax.axis("off")

    return legend


def plot_cost_bubble(df):
    """
    'Bubble' plot to illustrate the relative importance of our cost components
    in the presence and absence of diabetes. Effectively a scatter plot of their
    mean contribution to the net cost of a spell where the size of the marker is
    proportional to its coefficient of variation.
    """
    fontsize = 20

    nondiabetic = df[df["Diabetes"] == 0]
    diabetic = df[df["Diabetes"] == 1]

    args = zip(
        get_contribution_variation(nondiabetic).iterrows(),
        get_contribution_variation(diabetic).iterrows(),
    )

    fig, (ax, size_ax) = plt.subplots(
        ncols=2, figsize=(24, 12), dpi=400, gridspec_kw={"width_ratios": [16, 1]}
    )

    for nondiab_row, diab_row in args:

        contributions, i = [], 0
        for i, (component, point) in enumerate([nondiab_row, diab_row]):

            if i == 0:
                face, centre = blue, blue
            else:
                face, centre = green, "w"

            contribution = point["contribution"]
            variation = abs(point["variation"])
            contributions.append(contribution)
            ax.scatter(
                component,
                contribution,
                s=1e3 * variation,
                marker=".",
                zorder=2.5 - (0.01 * variation),
                alpha=0.75,
                edgecolor="None",
                facecolor=face,
            )
            ax.scatter(
                component,
                contribution,
                s=100,
                marker=".",
                zorder=2.5 - (0.01 * variation),
                color=centre,
            )

        ax.vlines(nondiab_row[0], -1, min(contributions), "grey", "dotted")

    legend = make_legend(ax)
    size_legend = make_size_legend(size_ax)

    ax.set_ylabel("Average proportion of net cost", fontsize=fontsize)
    ax.set_ylim(-0.1, 0.3)
    ax.set_xlim(-1.5, 25.5)

    ax.set_axisbelow(True)
    ax.grid(b=True, which="major", axis="y")
    ax.set_yticks(ax.get_yticks()[1:-1])

    ax.set_xlim(ax.get_xlim())
    ax.hlines(0, *ax.get_xlim(), color="darkgray", lw=2)

    for label in ax.get_yticklabels():
        label.set_fontsize(fontsize * 0.8)

    for label in ax.get_xticklabels():
        label.set_fontsize(fontsize * 0.8)
        label.set_rotation(45)
        label.set_horizontalalignment("right")

    plt.tight_layout()

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.savefig(filename, transparent=True)
