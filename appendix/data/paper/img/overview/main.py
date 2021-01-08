""" Main script for overview plot generation. """

import json
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sbn
from age_bar.main import plot_age_bar
from corr_heatmap.main import plot_corr_heatmap
from cost_bubble_plot.main import plot_cost_bubble
from cost_contribution.main import plot_cost_contribution
from cost_variation.main import plot_cost_variation
from dask import compute, delayed
from los_bar.main import plot_los_bar
from netcost_kde.main import plot_netcost_kde
from no_diag_bar.main import plot_no_diag_bar
from no_proc_bar.main import plot_no_proc_bar
from no_spells_bar.main import plot_no_spells_bar


def main(num_cores):
    """
    Generate all plots for overview of data.
    """
    sbn.set_palette("colorblind")
    sbn.set_style("ticks")

    plt.rcParams["axes.labelpad"] = 10
    plt.rcParams["axes.labelsize"] = "xx-large"
    plt.rcParams["xtick.labelsize"] = "xx-large"
    plt.rcParams["ytick.labelsize"] = "xx-large"

    plt.rcParams["legend.title_fontsize"] = "xx-large"
    plt.rcParams["legend.fontsize"] = "x-large"

    with open("/Volumes/thesis-data/dtype_dict.json", "r") as dtypes:
        dtypes = json.load(dtypes)

    dataframe = pd.read_csv(
        "/Volumes/thesis-data/main.csv",
        dtype=dtypes,
        parse_dates=["PERIOD", "ADMDATE", "DISCDATE"],
    )

    plots = [
        plot_age_bar,
        plot_corr_heatmap,
        plot_cost_bubble,
        plot_cost_contribution,
        plot_cost_variation,
        plot_los_bar,
        plot_netcost_kde,
        plot_no_diag_bar,
        plot_no_proc_bar,
        plot_no_spells_bar,
    ]

    tasks = [delayed(plot(dataframe)) for plot in plots]
    compute(tasks, scheduler="processes", num_workers=num_cores)


if __name__ == "__main__":
    CORES = int(sys.argv[1])
    main(CORES)
