from collections import Counter

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_age_bar(df):
    """
    Bar chart for the age of patients.
    """
    ages = df.drop_duplicates("SPELL_ID")["Age"].dropna().values
    fontsize = 16
    width = 0.45
    data = Counter(ages)

    uk_age = pd.read_csv(
        "/Volumes/thesis-data/rsc/UK_Age_2016.csv", usecols=["2016"]
    )
    uk_data = np.array(uk_age.values).flatten()

    fig, ax = plt.subplots(1, figsize=(20, 8), dpi=300)

    ax.bar(
        np.array(list(data.keys())) - 0.5 * width,
        np.array(list(data.values())) / len(ages),
        width=width,
        label="CTHB data",
    )
    ax.bar(
        np.array(list(uk_age.index)) + 0.5 * width,
        uk_data / uk_data.sum(),
        width=width,
        label="UK population (c. 2016)",
    )

    ax.set_xlabel("Age", fontsize=fontsize)
    ax.set_ylabel("Frequency density", fontsize=fontsize)
    ax.legend(fontsize=fontsize * .8)

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(fontsize * .8)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
