import os

from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_palette('colorblind')

def main(df):
    """
    Histograms for number of procedures in an episode for diabetic and
    non-diabetic patients.
    """
    diab_nums = df[df['Diabetes'] == 1].set_index('EPISODE_ID')['PROC_NO']
    nondiab_nums = df[df['Diabetes'] == 0].set_index('EPISODE_ID')['PROC_NO']

    fig, axes = plt.subplots(2, figsize=(14, 10), dpi=300)

    bins = max(diab_nums.max(), nondiab_nums.max())
    args = zip(
        axes, ['Frequency', 'Frequency density'], [False, True], [100000, 0.05]
    )

    for ax, label, density, locs in args:

        ax.hist([nondiab_nums.values, diab_nums.values], bins,
                rwidth=0.9, density=density)

        minor_locs = MultipleLocator(locs)
        ax.yaxis.set_minor_locator(minor_locs)
        ax.set_axisbelow(True)
        ax.grid(b=True, which='minor', axis='y')

        ax.set_ylabel(label)
        ax.set_xlabel('Number of procedures')
        ax.legend(['non-diabetic', 'diabetic'], loc='best', fontsize=12)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
