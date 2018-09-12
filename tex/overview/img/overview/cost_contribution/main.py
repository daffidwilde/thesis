import os

from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt


def plot_cost_contribution(df):
    """
    Bar plot for the average contribution to the net cost of a spell
    """
    fontsize = 14
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
    summed_costs = df.groupby("SPELL_ID")[costs].sum()
    contributions = summed_costs[components].divide(
        summed_costs["NetCost"], axis=0
    )

    corr = summed_costs.corr()
    order = sorted(corr.columns, key=lambda col: abs(corr[col]).sum())[::-1]

    avg_contributions = contributions.mean()
    sorted_avg_contributions = avg_contributions.reindex(order).dropna()
    # sorted_avg_contributions = avg_contributions.sort_values(ascending=False)

    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    ax.bar(sorted_avg_contributions.index, sorted_avg_contributions.values)

    ax.set_axisbelow(True)
    ax.grid(b=True, which="major", axis="y")

    ax.set_xlim(ax.get_xlim())
    ax.hlines(0, *ax.get_xlim(), color='darkgray', lw=2)

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
