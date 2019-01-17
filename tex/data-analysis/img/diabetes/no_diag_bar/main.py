from collections import Counter

import os
import numpy as np
import matplotlib.pyplot as plt


def plot_no_diag_bar(df):
    """
    Figure showing density and frequency bar charts for no. of diagnoses in an
    episode. Here, we compare diabetic and non-diabetic patients.
    """
    fontsize = 14
    width = 0.45

    diab_nums = df[df["Diabetes"] == 1].set_index("EPISODE_ID")["DIAG_NO"]
    nondiab_nums = df[df["Diabetes"] == 0].set_index("EPISODE_ID")["DIAG_NO"]

    fig, (freq_ax, dens_ax) = plt.subplots(2, figsize=(14, 10), dpi=300)

    for data, label, shift in zip(
        [nondiab_nums, diab_nums],
        ['non-diabetic', 'diabetic'],
        [-.5 * width, .5 * width]
    ):

        data = Counter(data)

        freq_ax.bar(
            np.array(list(data.keys())) + shift,
            data.values(),
            width=width,
            label=label
        )

        dens_ax.bar(
            np.array(list(data.keys())) + shift,
            np.array(list(data.values())) / sum(data.values()),
            width=width,
            label=label
        )

    for ax, label in zip(
        [freq_ax, dens_ax], ['Frequency', 'Frequency density']
    ):
        ax.set_xlabel('Number of diagnoses', fontsize=fontsize)
        ax.set_ylabel(label, fontsize=fontsize)
        ax.legend(fontsize=fontsize * .8)

        for tick_label in ax.get_xticklabels() + ax.get_yticklabels():
            tick_label.set_fontsize(fontsize * .8)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
