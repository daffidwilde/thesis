import json

from dask import compute, delayed, get

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sbn

from admissions.main import plot_admissions
from age_hist.main import plot_age_hist
from corr_difference.main import plot_corr_differences
from corr_heatmap.main import plot_corr_heatmap
from corr_ratio.main import plot_corr_ratios
from corr_relative_change.main import plot_corr_relative_change
from cost_bubble_plot.main import plot_cost_bubble
from cost_contribution.main import plot_cost_contribution
from cost_variation.main import plot_cost_variation
from large_component_boxplots.main import plot_large_component_boxplots
from large_component_violinplots.main import plot_large_component_violinplots
from los_hist.main import plot_los_hist
from los_time.main import plot_los_time
from medium_component_boxplots.main import plot_medium_component_boxplots
from medium_component_violinplots.main import plot_medium_component_violinplots
from netcost_kde.main import plot_netcost_kde
from netcost_proportions.main import plot_netcost_proportions
from no_diag_hist.main import plot_no_diag_hist
from no_proc_hist.main import plot_no_proc_hist
from no_spells_hist.main import plot_no_spells_hist
from nodist_component_boxplots.main import plot_nodist_component_boxplots
from small_component_boxplots.main import plot_small_component_boxplots
from small_component_violinplots.main import plot_small_component_violinplots

def main():
    """
    Generate all plots for diabetic patient analysis.
    """
    plt.rcParams.update({'font.size': 16})
    sbn.set_palette('colorblind')
    with open('/Volumes/thesis-data/dtype_dict.json') as f:
        dtypes = json.load(f)

    df = pd.read_csv('/Volumes/thesis-data/main.csv', dtype=dtypes,
                     parse_dates=['PERIOD', 'ADMDATE', 'DISCDATE'])

    plots = [
        plot_admissions, plot_age_hist, plot_corr_differences,
        plot_corr_heatmap, plot_corr_ratios, plot_corr_relative_change,
        plot_cost_bubble, plot_cost_contribution, plot_cost_variation,
        plot_large_component_boxplots, plot_large_component_violinplots,
        plot_los_hist, plot_los_time, plot_medium_component_boxplots,
        plot_medium_component_violinplots, plot_netcost_kde,
        plot_netcost_proportions, plot_no_diag_hist, plot_no_proc_hist,
        plot_no_spells_hist, plot_nodist_component_boxplots,
        plot_small_component_boxplots, plot_small_component_violinplots
    ]

    tasks = [delayed(plot(df)) for plot in plots]
    compute(tasks, get=get, num_workers=4)

if __name__ == '__main__':
    main()
