import os
import matplotlib.pyplot as plt


def plot_cost_variation(df):
    """
    Bar plot for the coefficient of variation in each cost component
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

    summed_costs = df.groupby("SPELL_ID")[costs].sum()

    corr = summed_costs.corr()
    order = sorted(corr.columns, key=lambda col: abs(corr[col]).sum())[::-1]

    variations = summed_costs.std() / summed_costs.mean()
    sorted_variations = variations.reindex(order).dropna()

    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    ax.bar(sorted_variations.index, sorted_variations.values)

    ax.set_ylabel(r"Coefficient of variation ($C_v$)")

    ax.set_axisbelow(True)
    ax.grid(b=True, which="major", axis="y")

    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment("right")

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
