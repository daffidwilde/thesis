import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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


def plot_cost_contribution(df):
    """
    Bar plot showing the mean contribution to the net cost of a spell for each
    of our cost components in the presence and absence of diabetes.
    """
    fontsize = 14
    width = 0.45

    nondiabetic = df[df["Diabetes"] == 0]
    diabetic = df[df["Diabetes"] == 1]

    contributions = []
    for dataset in (nondiabetic, diabetic):

        summed_costs = dataset.groupby("SPELL_ID")[costs].sum()
        netcost = summed_costs["NetCost"]
        contribution = summed_costs[components].divide(netcost, axis=0).mean()
        contributions.append(contribution)

    corr = summed_costs.corr()
    order = sorted(corr.columns, key = lambda col: abs(corr[col]).sum())[::-1]

    combined_contributions = (
        pd.concat(contributions, axis=1)
        .rename({0: "non-diabetic", 1: "diabetic"}, axis=1)
    )
    combined_contributions = combined_contributions.reindex(order).dropna()

    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    inds = np.arange(len(combined_contributions))
    for label, shift in zip(
        combined_contributions.columns, [-0.5 * width, 0.5 * width]
    ):
        data = combined_contributions[label]
        ax.bar(inds + shift, data.values, width, label=label)

    ax.set_axisbelow(True)
    ax.grid(b=True, which="major", axis="y")

    ax.set_xlim(ax.get_xlim())
    ax.hlines(0, *ax.get_xlim(), color='darkgray', lw=2)

    ax.legend(fontsize=fontsize * .8)
    ax.set_xticks(inds)
    ax.set_xticklabels(combined_contributions.index)
    ax.set_ylabel("Average proportion of net cost", fontsize=fontsize)
    for label in ax.get_yticklabels():
        label.set_fontsize(fontsize * .8)
    for label in ax.get_xticklabels():
        label.set_fontsize(fontsize * .8)
        label.set_rotation(45)
        label.set_horizontalalignment("right")

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
