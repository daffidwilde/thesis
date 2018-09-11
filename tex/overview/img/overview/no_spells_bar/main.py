from collections import Counter

import os

import matplotlib.pyplot as plt
import numpy as np


def plot_no_spells_bar(df):
    """
    Bar chart for no. of spells per patient.
    """
    no_spells = df.groupby("PATIENT_ID")["SPELL_ID"].nunique().values
    fontsize = 16
    data = Counter(no_spells)

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    ax.bar(
        data.keys(), np.array(list(data.values())) / len(no_spells), width=0.9
    )
    freq_ax.bar(data.keys(), data.values(), width=0.9)

    ax.set_ylabel("Frequency density", fontsize=fontsize)
    freq_ax.set_ylabel("Frequency", fontsize=fontsize)
    ax.set_xlabel("Number of spells", fontsize=fontsize)
    ax.set_xlim(0, 14.5)

    for label in (
        ax.get_xticklabels() + ax.get_yticklabels() + freq_ax.get_yticklabels()
    ):
        label.set_fontsize(fontsize * .8)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
