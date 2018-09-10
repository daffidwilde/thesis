import os

from itertools import cycle

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sbn

sbn.set_palette('colorblind')
colours = cycle(sbn.color_palette())
blue = next(colours)
green = next(colours)

cols = sorted(['THER', 'PHAR', 'PATH_OTH', 'PATH', 'NID', 'NCI', 'IMG', 'DRUG'])

def plot_medium_component_boxplots(df):
    """
    Grouped boxplots for the cost components which show a medium distribution.
    """
    nondiabetic = df[df['Diabetes'] == 0]
    diabetic = df[df['Diabetes'] == 1]

    contributions = []
    for dataset in (nondiabetic, diabetic):
        summed_costs = dataset.groupby('SPELL_ID')[cols + ['NetCost']].sum()
        contribution = summed_costs[cols] / summed_costs['NetCost']
        contributions.append(contribution)

    fig, ax = plt.subplots(1, figsize=(40, 24), dpi=400)

    pos = np.arange(len(cols)) * 1.5
    args = zip(['non-diabetic', 'diabetic'], contributions,
               [blue, green], [0.3, -0.3])

    patches = []
    for name, dataset, colour, beta in args:
        ax.boxplot([dataset[col] for col in cols], positions=pos+beta,
                   notch=True, sym='', vert=False, showmeans=True,
                   patch_artist=True, medianprops={'color': 'k'},
                   meanprops={'marker': 'o', 'markersize': 12})

        patch = mpatches.Patch(color=colour, label=name)
        patches.append(patch)

    ax.set_yticks(pos)
    ax.set_yticklabels(cols, fontsize=24)
    ax.set_xticks(ax.get_xticks()[1:-1])
    ax.set_xlabel('Proportion of net cost', fontsize=24)
    ax.set_ylabel('')
    ax.set_ylim(-1, int(pos[-1])+1)
    ax.legend(handles=patches, loc='best', fontsize=24, markerscale=24/8)
    for label in ax.get_xticklabels():
        label.set_fontsize(24)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename, transparent=True)
