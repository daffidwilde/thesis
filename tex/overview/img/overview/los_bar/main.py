from collections import Counter

import os
import numpy as np
import matplotlib.pyplot as plt


def plot_los_bar(df):
    """
    Bar chart for the spell-wise length of stay of patients in the dataset.
    """

    lengths = (
        df.set_index("ADMDATE").drop_duplicates("SPELL_ID")["TRUE_LOS"].dropna()
    )
    fontsize = 16
    data = Counter(lengths)

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    ax.bar(data.keys(), np.array(list(data.values())) / len(lengths), width=0.9)
    freq_ax.bar(data.keys(), data.values(), width=0.9)

    ax.set_ylabel("Frequency density", fontsize=fontsize)
    freq_ax.set_ylabel("Frequency", fontsize=fontsize)
    ax.set_xlabel("Length of stay (days)", fontsize=fontsize)
    ax.set_xlim(-1, 21.5)
    ax.set_xticks(np.arange(11) * 2)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
