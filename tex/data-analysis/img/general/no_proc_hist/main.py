import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sbn

sbn.set_palette('colorblind')

def main(df):
    """
    Histogram for the no. of procedures in an episode
    """
    procedure_nums = df.set_index('EPISODE_ID').PROC_NO

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    ax.hist(procedure_nums, procedure_nums.max(), rwidth=0.9, density=True)
    freq_ax = ax.twinx()
    freq_ax.hist(procedure_nums, procedure_nums.max(), rwidth=0.9)

    ax.set_ylabel('Frequency density')
    freq_ax.set_ylabel('Frequency')

    ax.set_xlabel('Number of procedures')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)