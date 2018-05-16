import os

from itertools import cycle
from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sbn

sbn.set_palette('colorblind')
colours = cycle(sbn.color_palette())
blue = next(colours)

def main(df):
    """
    'Bubble' plot to illustrate the relative importance of our cost components.
    Effectively, a scatter plot of the average contribution to net cost of a
    spell for each component where the size of the marker is proportional to the
    corresponding coefficient of variation.
    """
    np.random.seed(3)

    costs = ['COST', 'NetCost', 'DRUG', 'ENDO', 'HCD', 'EMER', 'CRIT',
             'IMG', 'IMG_OTH', 'MED', 'NCI', 'NID', 'OCLST', 'OPTH',
             'OTH', 'OTH_OTH', 'OUTP', 'OVH', 'PATH', 'PATH_OTH',
             'PHAR', 'PROS', 'RADTH', 'SECC', 'SPS', 'THER', 'WARD']

    components = costs[2:]
    summed_costs = df.groupby('SPELL_ID')[costs].sum()
    variations = summed_costs.std() / summed_costs.mean()
    contributions = summed_costs[components].divide(summed_costs['NetCost'],
                                                    axis=0)
    avg_contributions = contributions.mean()

    cont_vars = pd.concat([avg_contributions, variations[components]], axis=1)\
                  .rename({0: 'contribution', 1: 'variation'}, axis=1)

    new_idx = np.random.permutation(cont_vars.index)
    cont_vars = cont_vars.reindex(new_idx)


    fig, (ax, size_ax) = plt.subplots(ncols=2, figsize=(24, 12), dpi=400,
                                      gridspec_kw={'width_ratios': [16, 1]})

    # Actual plot
    for point in cont_vars.iterrows():
        variation = abs(point[1]['variation'])
        ax.scatter(point[0], point[1]['contribution'], s=1e3*variation,
                   marker='.', zorder=2.5-(0.01*variation), alpha=0.75,
                   edgecolor='None', facecolor=blue)
        ax.scatter(point[0], point[1]['contribution'], s=100,
                   marker='.', zorder=2.5-(0.01*variation), color='w')
        ax.vlines(point[0], -1, point[1]['contribution'], 'grey', 'dotted')

    # Size legend
    for size in [2, 5, 10, 25, 40]:
        size_ax.scatter([], [], marker='.', s=1e3*size, alpha=0.75,
                        facecolor=blue, edgecolor='None', label=size)

    handles, labels = size_ax.get_legend_handles_labels()
    size_lgnd = size_ax.legend(handles, labels,
                               title=r'Coefficient of'+'\n'+'variation ($C_v$)',
                               labelspacing=5.5, loc='best', fontsize=20,
                               handletextpad=4, edgecolor='None')

    size_lgnd.get_title().set_fontsize(24)
    size_lgnd._legend_box.sep = 60
    size_ax.set_xlim(0, 0.04)
    size_ax.axis('off')

    # Settings
    ax.set_ylabel('Average proportion of net cost', fontsize=20)
    ax.set_ylim(-0.1, 0.3)
    ax.set_xlim(-1.5, 25.5)

    ax.set_axisbelow(True)
    ax.grid(b=True, which='major', axis='y')
    ax.set_yticks(ax.get_yticks()[1:-1])

    for label in ax.get_yticklabels():
        label.set_fontsize(16)

    for label in ax.get_xticklabels():
        label.set_fontsize(16)
        label.set_rotation(45)
        label.set_horizontalalignment('right')

    plt.tight_layout()

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
