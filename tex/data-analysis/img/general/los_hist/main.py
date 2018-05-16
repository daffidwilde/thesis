import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sbn

sbn.set_palette('colorblind')

def main(df):
    """
    Histogram for the spell-wise length of stay of patients in the dataset.
    """
    time_constraint = (df['ADMDATE'] >= '2012-04-01') \
                      & (df['DISCDATE'] < '2017-04-31')

    lengths = df[time_constraint].set_index('ADMDATE') \
                                 .drop_duplicates('SPELL_ID')['TRUE_LOS'] \
                                 .dropna()

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    bins = int(lengths.max())
    ax.hist(lengths, bins, rwidth=0.9, density=True)
    freq_ax.hist(lengths, bins, rwidth=0.9)

    ax.set_xlim(-0.5, 21)
    ax.set_xticks(np.arange(1, 21))
    ax.set_xlabel('Length of stay (days)')
    ax.set_ylabel('Frequency density')
    freq_ax.set_ylabel('Frequency')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(filename)
    plt.savefig(filename)
