import os

from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt
import numpy as np

def plot_los_hist(df):
    """
    Histograms for the lengths of stay of diabetic and non-diabetic patients.
    """
    time_constraint = (df['ADMDATE'] >= '2012-04-01') \
                      & (df['DISCDATE'] < '2017-04-30')

    diab_lengths = df[(df['Diabetes'] == 1) \
                      & (time_constraint)].set_index('ADMDATE') \
                      .drop_duplicates('SPELL_ID')['TRUE_LOS'].dropna()
    nondiab_lengths = df[(df['Diabetes'] == 0) \
                         & (time_constraint)].set_index('ADMDATE') \
                         .drop_duplicates('SPELL_ID')['TRUE_LOS'].dropna()

    fig, axes = plt.subplots(2, figsize=(14, 10), dpi=300)

    bins = int(max(diab_lengths.max(), nondiab_lengths.max()))
    args = zip(
        axes, ['Frequency', 'Frequency density'], [False, True], [100000, 0.05]
    )

    for ax, label, density, locs in args:

        ax.hist([nondiab_lengths.values, diab_lengths.values], bins,
                rwidth=0.9, density=density)

        minor_locs = MultipleLocator(locs)
        ax.yaxis.set_minor_locator(minor_locs)
        ax.set_axisbelow(True)
        ax.grid(b=True, which='minor', axis='y')

        ax.set_xticks(np.arange(1, 22))
        ax.set_xlim(-0.5, 22)
        ax.set_xlabel('Length of stay (days)')
        ax.set_ylabel(label)
        ax.legend(['non-diabetic', 'diabetic'], loc='best', fontsize=12)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename, transparent=True)
