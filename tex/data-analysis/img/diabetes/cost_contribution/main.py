import os

from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


costs = ['COST', 'NetCost', 'DRUG', 'ENDO', 'HCD', 'EMER', 'CRIT',
         'IMG', 'IMG_OTH', 'MED', 'NCI', 'NID', 'OCLST', 'OPTH',
         'OTH', 'OTH_OTH', 'OUTP', 'OVH', 'PATH', 'PATH_OTH',
         'PHAR', 'PROS', 'RADTH', 'SECC', 'SPS', 'THER', 'WARD']

components = costs[2:]


def plot_cost_contribution(df):
    """
    Bar plot showing the mean contribution to the net cost of a spell for each
    of our cost components in the presence and absence of diabetes.
    """

    nondiabetic = df[df['Diabetes'] == 0]
    diabetic = df[df['Diabetes'] == 1]

    contributions = []
    for dataset in (nondiabetic, diabetic):

        summed_costs = dataset.groupby('SPELL_ID')[costs].sum()
        netcost = summed_costs['NetCost']
        contribution = summed_costs[components].divide(netcost, axis=0).mean()
        contributions.append(contribution)

    combined_contributions = pd.concat(contributions, axis=1) \
                               .rename({0: 'nondiab', 1: 'diab'}, axis=1) \
                               .sort_values('nondiab', ascending=False)


    fig, ax = plt.subplots(1, figsize=(14, 10), dpi=300)

    width = 0.4
    inds = np.arange(len(combined_contributions))

    ax.bar(inds, combined_contributions['nondiab'].values,
           width, label='non-diabetic')
    ax.bar(inds+width, combined_contributions['diab'].values,
           width, label='diabetic')

    minor_locs = MultipleLocator(0.025)
    ax.yaxis.set_minor_locator(minor_locs)
    ax.set_axisbelow(True)
    ax.grid(b=True, which='minor', axis='y')

    ax.set_xticks(inds + width/2)
    ax.set_xticklabels(combined_contributions.index)
    ax.set_ylabel('Average proportion of net cost')
    ax.legend(loc='best')
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment('right')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
