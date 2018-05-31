import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sbn

def plot_corr_ratios(df):
    """
    Heatmap showing the ratio of the pairwise correlation coefficients of
    our cost components and some other clinical variables at the spell level,
    between diabetic patients and the general dataset.
    """
    costs = ['COST', 'NetCost', 'DRUG', 'ENDO', 'HCD', 'EMER', 'CRIT',
             'IMG', 'IMG_OTH', 'MED', 'NCI', 'NID', 'OCLST', 'OPTH',
             'OTH', 'OTH_OTH', 'OUTP', 'OVH', 'PATH', 'PATH_OTH',
             'PHAR', 'PROS', 'RADTH', 'SECC', 'SPS', 'THER', 'WARD']

    diabetic = df[df['Diabetes'] == 1]

    corrs = []
    for dataset in (diabetic, df):

        summed_costs = dataset.groupby('SPELL_ID')[costs].sum()
        lengths_of_stay = dataset.groupby('SPELL_ID')['TRUE_LOS'].mean()
        max_diagnosis_nums = dataset.groupby('SPELL_ID')['DIAG_NO'].max()
        summed_procedure_nums = dataset.groupby('SPELL_ID')['PROC_NO'].sum()

        data = pd.concat([summed_costs, lengths_of_stay, max_diagnosis_nums,
                          summed_procedure_nums], axis=1)

        correlation = data.corr().round(2)
        corrs.append(correlation)

    ratio = corrs[0] / corrs[1]
    ratio.replace([-np.infty, np.infty], np.nan, inplace=True)

    fig, ax = plt.subplots(1, figsize=(12, 10), dpi=400)

    sbn.heatmap(ratio, square=True, cmap='RdBu', center=1, lw=0.01,
                annot=True, annot_kws={'fontsize': 6}, ax=ax)

    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment('right')

    ax.set_title('Ratio of correlation coefficients for diabetic patients'\
                 ' and the general population \n')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
