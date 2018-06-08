import os

from itertools import cycle
from scipy.stats import gaussian_kde

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sbn

sbn.set_palette('colorblind')
colours = cycle(sbn.color_palette())
blue = next(colours)
green = next(colours)

cols = sorted(['THER', 'PHAR', 'PATH_OTH', 'PATH', 'NID', 'NCI', 'IMG', 'DRUG'])
fontsize = 24
delta = 0.05
steps = 200
xmin, xmax = 0, 0.25
positions = np.arange(len(cols)) * 1.5

def get_contributions(df, boolean):
    """
    Get the mean contribution of each cost component to the net cost of a spell
    conditioned on some binary (Boolean) variable. Here, we use diabetes.
    """
    dataset = df[df['Diabetes'] == boolean]
    summed_costs = dataset.groupby('SPELL_ID')[cols].sum()
    netcost = dataset.groupby('SPELL_ID')['NetCost'].sum()
    contribution = summed_costs.divide(netcost, axis=1).mean()

    return contribution

def get_vpstats(df, col):
    """
    Return a dictionary to be passed to the violin plotter.
    """
    data = df[col].values
    coords = np.linspace(xmin, xmax, steps)
    density = gaussian_kde(data)

    if col == 'NCI':
        coords *= -1

    mean = np.mean(data)
    LQ = np.percentile(data, 25)
    UQ = np.percentile(data, 75)
    median = np.median(data)

    stats = {
        'coords': coords, 'vals': density(coords), 'mean': mean,
        'min': LQ, 'max': UQ, 'median': median
    }

    return stats

def plot_medium_component_violinplots(df):
    """
    Plot horizontal violins for the cost components that make a medium
    contribution to the mean net cost of a spell, hued on the presence or
    absence of diabetes.
    """
    fig, ax = plt.subplots(1, figsize=(40, 24), dpi=400)

    contributions = [get_contributions(df, i) for i in [0, 1]]
    args = zip(['non-diabetic', 'diabetic'], contributions,
               [blue, green], [0.3, -0.3])

    patches = []
    for name, contribution, colour, beta in args:

        vpstats = []
        for i, col in enumerate(cols):
            pos = positions[i] + beta
            stats = get_vpstats(contribution, col)

            IQR = stats['max'] - stats['min']
            lower_whisker = max(xmin, stats['min']-1.5*IQR)
            upper_whisker = min(xmax, stats['max']+1.5*IQR)

            if col == 'NCI':
                lower_whisker = max(-xmax, stats['min']-1.5*IQR)
                upper_whisker = min(xmin, stats['max']+1.5*IQR)

            vpstats.append(stats)

            ax.hlines(pos, stats['min'], stats['max'], lw=7, color='k')
            ax.hlines(pos, lower_whisker, upper_whisker, lw=1, color='k')
            ax.vlines(lower_whisker, pos-delta, pos+delta, lw=1, color='k')
            ax.vlines(upper_whisker, pos-delta, pos+delta, lw=1, color='k')
            ax.scatter(stats['median'], pos, s=50, color='w', zorder=100)

        patch = mpatches.Patch(color=colour, label=name)
        patches.append(patch)

        ax.violin(vpstats, vert=False, positions=positions+beta,
                  showmedians=False, showextrema=False)

    ax.set_yticks(positions)
    ax.set_yticklabels(cols, fontsize=fontsize)
    ax.set_xlabel('Proportion of net cost', fontsize=fontsize)
    ax.legend(handles=patches, loc='best', fontsize=fontsize,
              markerscale=fontsize/8)
    for label in ax.get_xticklabels():
        label.set_fontsize(fontsize)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename, transparent=True)
