import os

from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


costs = ['COST', 'NetCost', 'DRUG', 'ENDO', 'HCD', 'EMER', 'CRIT',
         'IMG', 'IMG_OTH', 'MED', 'NCI', 'NID', 'OCLST', 'OPTH',
         'OTH', 'OTH_OTH', 'OUTP', 'OVH', 'PATH', 'PATH_OTH',
         'PHAR', 'PROS', 'RADTH', 'SECC', 'SPS', 'THER', 'WARD']


def plot_cost_variation(df):
    """
    Bar plot for the coefficient of variation in each cost component split by
    the presence of diabetes
    """

    nondiabetic = df[df['Diabetes'] == 0]
    diabetic = df[df['Diabetes'] == 1]

    variations = []
    for dataset in (nondiabetic, diabetic):
        summed_costs = dataset.groupby('SPELL_ID')[costs].sum()
        variation = summed_costs.std() / summed_costs.mean()
        variations.append(variation)

    combined_variations = pd.concat(variations, axis=1) \
                            .rename({0: 'nondiab', 1: 'diab'}, axis=1) \
                            .sort_values('nondiab', ascending=False)


    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    width = 0.4
    inds = np.arange(len(combined_variations))

    ax.bar(inds, combined_variations['nondiab'].values,
           width, label='non-diabetic')
    ax.bar(inds+width, combined_variations['diab'].values,
           width, label='diabetic')

    minor_locs = MultipleLocator(5)
    ax.yaxis.set_minor_locator(minor_locs)
    ax.set_axisbelow(True)
    ax.grid(b=True, which='minor', axis='y')

    ax.set_xticks(inds + width/2)
    ax.set_xticklabels(combined_variations.index)
    ax.set_ylabel(r' Coefficient of variation ($C_v$)', fontsize=12)
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment('right')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
