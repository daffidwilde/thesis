import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from seaborn import color_palette


def plot_age_bar(df):
    """
    Bar chart for the age of patients.
    """
    ages = df.drop_duplicates("SPELL_ID")["Age"].dropna().values
    width = 0.45
    data = Counter(ages)

    blue, orange = [color_palette("colorblind")[i] for i in [0, 2]]

    uk_age = pd.read_csv("/Volumes/thesis-data/rsc/UK_Age_2016.csv", usecols=["2016"])
    uk_data = np.array(uk_age.values).flatten()

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)

    ax.bar(
        np.array(list(data.keys())) - 0.5 * width,
        np.array(list(data.values())) / len(ages),
        width=width,
        color=blue,
        label="CTHB data",
    )
    ax.bar(
        np.array(list(uk_age.index)) + 0.5 * width,
        uk_data / uk_data.sum(),
        width=width,
        color=orange,
        label="UK population (c. 2016)",
    )

    ax.set_xlabel("Age")
    ax.set_ylabel("Frequency density")
    ax.legend()
    ax.set_xlim(-5, 105)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
