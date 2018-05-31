import os

from scipy.stats import gaussian_kde

import matplotlib.pyplot as plt
import numpy as np

def plot_netcost_kde(df):
    """
    Plot both KDEs for the net cost of a spell in the presence and absence of
    diabetes on the same axis.
    """
    fig, ax = plt.subplots(1, figsize=(14, 10), dpi=300)

    steps = 300
    xs = np.linspace(0, 12500, steps)

    for i, name in enumerate(['non-diabetic', 'diabetic']):
        data = df[df['Diabetes'] == i]
        netcost = data.groupby('SPELL_ID')['NetCost'].sum()
        density = gaussian_kde(netcost)

        ax.plot(xs, density(xs), label=name)
        ax.fill_between(xs, [0]*steps, density(xs), alpha=0.1)

    ax.set_xlabel('Net cost of a spell')
    ax.set_ylabel('Estimated probability density')
    ax.legend(loc='best')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
