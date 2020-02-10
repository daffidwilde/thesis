import os

import matplotlib.pyplot as plt


def plot_cost_contribution(df):
    """
    Bar plot for the average contribution to the net cost of a spell
    """
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

    mean_contributions = contributions.mean()
    mean_contributions = mean_contributions.reindex(order).dropna()

    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    ax.bar(mean_contributions.index, mean_contributions.values)

    ax.set_ylabel("Mean proportion of net cost")

    ax.set_axisbelow(True)
    ax.grid(b=True, which="major", axis="y")

    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment("right")

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
