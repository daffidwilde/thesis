import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sbn

def main(df):
    """
    Heatmap showing the pairwise correlation coefficients of our cost components
    and some other clinical variables at the spell level.
    """
    costs = ['COST', 'NetCost', 'DRUG', 'ENDO', 'HCD', 'EMER', 'CRIT',
             'IMG', 'IMG_OTH', 'MED', 'NCI', 'NID', 'OCLST', 'OPTH',
             'OTH', 'OTH_OTH', 'OUTP', 'OVH', 'PATH', 'PATH_OTH',
             'PHAR', 'PROS', 'RADTH', 'SECC', 'SPS', 'THER', 'WARD']

    summed_costs = df.groupby('SPELL_ID')[costs].sum()
    lengths_of_stay = df.groupby('SPELL_ID')['TRUE_LOS'].mean()
    max_diagnosis_nums = df.groupby('SPELL_ID')['DIAG_NO'].max()
    summed_procedure_nums = df.groupby('SPELL_ID')['PROC_NO'].sum()

    data = pd.concat([summed_costs, lengths_of_stay, max_diagnosis_nums,
                      summed_procedure_nums], axis=1)

    correlation = data.corr().round(2)


    fig, ax = plt.subplots(1, figsize(12, 10), dpi=400)

    sbn.heatmap(correlation, square=True, cmap='viridis', center=0, lw=0.01,
                annot=True, annot_kws={'fontsize': 6}, ax=ax)

    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment('right')

    ax.set_title('Correlation coefficients for spell-level cost components and \
                  other clinical variables \n')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)