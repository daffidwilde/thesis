import os

import matplotlib.pyplot as plt

def plot_age_hist(df):
    """
    Histogram for the age of patients.
    """
    ages = df.drop_duplicates('SPELL_ID')['Age'].dropna().values

    fig, ax = plt.subplots(1, figsize=(14, 8), dpi=300)
    freq_ax = ax.twinx()

    bins = int(ages.max() / 2)
    ax.hist(ages, bins, rwidth=0.9, density=True)
    freq_ax.hist(ages, bins, rwidth=0.9)

    ax.set_xlabel('Age (2 year bins)')
    ax.set_ylabel('Frequency density')
    freq_ax.set_ylabel('Frequency')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
