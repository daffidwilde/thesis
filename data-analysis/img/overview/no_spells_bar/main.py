import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np


def plot_no_spells_bar(df):
    """
    Bar chart for no. of spells per patient.
    """
    no_spells = df.groupby("PATIENT_ID")["SPELL_ID"].nunique().values

    data = Counter(no_spells)

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    ax.bar(data.keys(), np.array(list(data.values())) / len(no_spells), width=0.9)
    freq_ax.bar(data.keys(), np.array(list(data.values())) / 100000, width=0.9)

    ax.set_ylabel("Frequency density")
    freq_ax.set_ylabel("Frequency (100,000's)")
    ax.set_xlabel("Number of spells")
    ax.set_xlim(0, 14.5)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
