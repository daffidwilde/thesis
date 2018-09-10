import os

import matplotlib.pyplot as plt
import numpy as np

def plot_no_spells_hist(df):
    """
    Histogram for no. of spells per patient.
    """
    no_spells = df.groupby('PATIENT_ID')['SPELL_ID'].nunique().values

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    ax.hist(no_spells, no_spells.max(), rwidth=0.9, density=True)
    freq_ax.hist(no_spells, no_spells.max(), rwidth=0.9)

    ax.set_ylabel('Frequency density')
    freq_ax.set_ylabel('Frequency')
    ax.set_xlabel('Number of spells')
    ax.set_xlim(0.5, 15)
    ax.set_xticks(np.arange(1, 15))

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename, transparent=True)
