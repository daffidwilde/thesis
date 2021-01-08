import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np


def plot_no_diag_bar(df):
    """
    Bar chart for the no. of diagnoses in a spell.
    """
    diag_nums = df.groupby("EPISODE_ID")["DIAG_NO"].max()

    data = Counter(diag_nums)

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    ax.bar(
        data.keys(), np.array(list(data.values())) / len(diag_nums), width=0.9
    )
    freq_ax.bar(data.keys(), np.array(list(data.values())) / 100000, width=0.9)

    ax.set_ylabel("Frequency density")
    freq_ax.set_ylabel("Frequency (100,000's)")
    ax.set_xlabel("Maximum number of diagnoses in spell")

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
