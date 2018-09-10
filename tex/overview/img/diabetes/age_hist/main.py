import os

from matplotlib.ticker import MultipleLocator

import matplotlib.pyplot as plt

def plot_age_hist(df):
    """
    Histograms for the age of diabetic and non-diabetic patients.
    """
    diab_ages = df[df['Diabetes'] == 1].set_index('PATIENT_ID') \
                                       .drop_duplicates('SPELL_ID')['Age'] \
                                       .dropna()
    nondiab_ages = df[df['Diabetes'] == 0].set_index('PATIENT_ID') \
                                          .drop_duplicates('SPELL_ID')['Age'] \
                                          .dropna()

    fig, axes = plt.subplots(2, figsize=(14, 10), dpi=300)

    bins = int(max(diab_ages.max(), nondiab_ages.max()) / 2)
    args = zip(
        axes, ['Frequency', 'Frequency density'], [False, True], [10000, 0.0025]
    )

    for ax, label, density, locs in args:

        ax.hist([nondiab_ages.values, diab_ages.values], bins,
                rwidth=0.9, density=density)

        minor_locs = MultipleLocator(locs)
        ax.minorticks_on()
        ax.yaxis.set_minor_locator(minor_locs)
        ax.set_axisbelow(True)
        ax.grid(b=True, which='minor', axis='y')

        ax.set_ylabel(label)
        ax.set_xlabel('Age (2 year bins)')
        ax.legend(['non-diabetic', 'diabetic'], loc='best', fontsize=12)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename, transparent=True)
