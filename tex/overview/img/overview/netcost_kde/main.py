from scipy.stats import gaussian_kde

import os
import numpy as np
import matplotlib.pyplot as plt


def plot_netcost_kde(df):
    """
    Gaussian KDE for net cost of a spell
    """
    netcost = df.groupby("SPELL_ID")["NetCost"].sum()
    fontsize = 16
    steps = 300
    xs = np.linspace(netcost.min(), 12500, steps)
    density = gaussian_kde(netcost)

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)

    ax.plot(xs, density(xs))
    ax.fill_between(xs, [0] * steps, density(xs), alpha=0.25)

    ax.set_xlabel("Net cost", fontsize=fontsize)
    ax.set_ylabel("Estimated probability density", fontsize=fontsize)

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(fontsize * .8)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
