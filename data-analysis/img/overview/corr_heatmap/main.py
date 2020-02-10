import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sbn


def plot_corr_heatmap(df):
    """
    Heatmap showing the pairwise correlation coefficients of our cost components
    and some other clinical variables at the spell level.
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
    lengths_of_stay = df.groupby("SPELL_ID")["TRUE_LOS"].mean()
    max_diagnosis_nums = df.groupby("SPELL_ID")["DIAG_NO"].max()
    summed_procedure_nums = df.groupby("SPELL_ID")["PROC_NO"].sum()

    data = pd.concat(
        [summed_costs, lengths_of_stay, max_diagnosis_nums, summed_procedure_nums],
        axis=1,
    )

    corr = data.corr().round(2)
    order = sorted(corr.columns, key=lambda col: abs(corr[col]).sum())[::-1]
    corr = corr[order].reindex(order)

    fig, ax = plt.subplots(1, figsize=(16, 12), dpi=400)

    sbn.heatmap(
        corr, square=True, cmap="viridis", vmin=-1, vmax=1, lw=0.01, annot=False, ax=ax
    )

    for label in ax.get_xticklabels():
        label.set_rotation(60)
        label.set_horizontalalignment("right")

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
