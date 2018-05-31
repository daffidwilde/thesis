import os

from scipy.stats import gaussian_kde

import matplotlib.pyplot as plt
import numpy as np

def plot_netcost_kde(df):
    """
    Gaussian KDE for net cost of a spell
    """
    netcost = df.groupby('SPELL_ID')['NetCost'].sum()
    steps = 300
    xs = np.linspace(netcost.min(), 12500, steps)
    density = gaussian_kde(netcost)

    fig, ax = plt.subplots(1, figsize=(14, 10), dpi=300)

    ax.plot(xs, density(xs))
    ax.fill_between(xs, [0]*steps, density(xs), alpha=0.25)

    ax.set_xlabel('Net cost of a spell')
    ax.set_ylabel('Estimated probability density')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
