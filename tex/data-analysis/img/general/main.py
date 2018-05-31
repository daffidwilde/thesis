import json

from dask import compute, delayed, get

import pandas as pd
import seaborn as sbn

from age_hist.main import plot_age_hist
from corr_heatmap.main import plot_corr_heatmap
from cost_bubble_plot.main import plot_cost_bubble
from cost_contribution.main import plot_cost_contribution
from cost_variation.main import plot_cost_variation
from los_hist.main import plot_los_hist
from netcost_kde.main import plot_netcost_kde
from no_diag_hist.main import plot_no_diag_hist
from no_proc_hist.main import plot_no_proc_hist
from no_spells_hist.main import plot_no_spells_hist

def main():
    """
    Generate all plots for general dataset analysis.
    """
    sbn.set_palette('colorblind')
    with open('/Volumes/thesis-data/dtype_dict.json', 'r') as f:
        dtypes = json.load(f)

    df = pd.read_csv('/Volumes/thesis-data/main.csv', dtype=dtypes,
                     parse_dates=['PERIOD', 'ADMDATE', 'DISCDATE'])

    plots = [
        plot_age_hist, plot_corr_heatmap, plot_cost_bubble,
        plot_cost_contribution, plot_cost_variation, plot_los_hist,
        plot_netcost_kde, plot_no_diag_hist, plot_no_proc_hist,
        plot_no_spells_hist
    ]

    tasks = [delayed(plot(df)) for plot in plots]
    compute(tasks, get=get)

if __name__ == '__main__':
    main()
