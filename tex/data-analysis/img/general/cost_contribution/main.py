import os

from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt

def plot_cost_contribution(df):
    """
    Bar plot for the average contribution to the net cost of a spell
    """
    costs = ['COST', 'NetCost', 'DRUG', 'ENDO', 'HCD', 'EMER', 'CRIT',
             'IMG', 'IMG_OTH', 'MED', 'NCI', 'NID', 'OCLST', 'OPTH',
             'OTH', 'OTH_OTH', 'OUTP', 'OVH', 'PATH', 'PATH_OTH',
             'PHAR', 'PROS', 'RADTH', 'SECC', 'SPS', 'THER', 'WARD']

    components = costs[2:]
    summed_costs = df.groupby('SPELL_ID')[costs].sum()
    contributions = summed_costs[components].divide(summed_costs['NetCost'],
                                                    axis=0)
    avg_contributions = contributions.mean()
    sorted_avg_contributions = avg_contributions.sort_values(ascending=False)

    fig, ax = plt.subplots(1, figsize=(14, 10), dpi=300)

    ax.bar(sorted_avg_contributions.index, sorted_avg_contributions.values)

    minor_locs = MultipleLocator(0.025)
    ax.yaxis.set_minor_locator(minor_locs)
    ax.set_axisbelow(True)
    ax.grid(b=True, which='minor', axis='y')

    ax.set_ylabel('Average proportion of net cost', fontsize=12)
    for label in ax.get_xticklabels():
        label.set_fontsize(12)
        label.set_rotation(45)
        label.set_horizontalalignment('right')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
