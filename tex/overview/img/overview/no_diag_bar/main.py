from collections import Counter

import os
import numpy as np
import matplotlib.pyplot as plt


def plot_no_diag_bar(df):
    """
    Bar chart for the no. of diagnoses in an episode.
    """
    diag_nums = df.set_index("EPISODE_ID")["DIAG_NO"]
    fontsize = 16
    data = Counter(diag_nums)

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    ax.bar(
        data.keys(), np.array(list(data.values())) / len(diag_nums), width=0.9
    )
    freq_ax.bar(data.keys(), data.values(), width=0.9)

    ax.set_ylabel("Frequency density", fontsize=fontsize)
    freq_ax.set_ylabel("Frequency", fontsize=fontsize)
    ax.set_xlabel("Number of diagnoses", fontsize=fontsize)

    for label in (
        ax.get_xticklabels() + ax.get_yticklabels() + freq_ax.get_yticklabels()
    ):
        label.set_fontsize(fontsize * .8)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
