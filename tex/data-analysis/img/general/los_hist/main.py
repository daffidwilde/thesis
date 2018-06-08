import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_los_hist(df):
    """
    Histogram for the spell-wise length of stay of patients in the dataset.
    """
    time_constraint = (df['ADMDATE'] >= pd.to_datetime('2012-04-01')) \
                      & (df['DISCDATE'] < pd.to_datetime('2017-04-30'))

    lengths = df[time_constraint].set_index('ADMDATE') \
                                 .drop_duplicates('SPELL_ID')['TRUE_LOS'] \
                                 .dropna()

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    bins = int(lengths.max())
    ax.hist(lengths, bins, rwidth=0.9, density=True)
    freq_ax.hist(lengths, bins, rwidth=0.9)

    ax.set_xlim(-0.5, 22)
    ax.set_xticks(np.arange(0, 22))
    ax.set_xlabel('Length of stay (days)')
    ax.set_ylabel('Frequency density')
    freq_ax.set_ylabel('Frequency')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename, transparent=True)
