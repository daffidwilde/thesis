import os

from matplotlib.dates import date2num
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_netcost_proportions(df):
    """
    A time series plot for the proportion diabetic patients make up of the total
    net cost of a spell by their admission date. See plot_los_time() for details
    on misrepresentation incurred.
    """
    fontsize = 16

    diabetic = df[df["Diabetes"] == 1]

    diabetic_netcost = diabetic.groupby("ADMDATE")["NetCost"].sum()
    total_netcost = df.groupby("ADMDATE")["NetCost"].sum()

    proportions = diabetic_netcost / total_netcost
    proportions.dropna(inplace=True)

    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    monthly = proportions.resample("BM").mean()
    yearly = proportions.resample("BA-APR").mean()
    yearly_err = monthly.resample("BA-APR").std().bfill()

    params = pd.DataFrame(yearly_err).rename({"NetCost": "err"}, axis=1)
    params["val"] = yearly.values
    params["vmin"] = params["val"] - params["err"]
    params["vmax"] = params["val"] + params["err"]

    X, y = (
        date2num(monthly.index.values.reshape(-1, 1)),
        monthly.values.reshape(-1, 1)
    )

    lr = LinearRegression()
    lr.fit(X, y)
    y_pred = lr.predict(X)

    linreg_df = pd.DataFrame(lr.predict(X), index=monthly.index)

    r_squared = np.round(r2_score(y, y_pred), 4)
    standard_err = np.round(np.sqrt((y - y_pred) ** 2).sum() / len(y), 4)

    ax.errorbar(
        params.index,
        params["val"],
        params["err"],
        capsize=8,
        alpha=0.25,
        ecolor="k",
        linestyle="",
        label="Standard dev.",
    )

    ax.plot(monthly, ".", alpha=0.75, label="End of month avg.")
    ax.plot(yearly, "x", label="End of year avg.")
    ax.plot(linreg_df, "-", label="Lin. regression model")

    ax.annotate(
        r'$R^2 = $ ' + str(r_squared) + '\n' + r'$SE = $ ' + str(standard_err),
        ['2012-05-01', 0.1445],
        fontsize=fontsize
    )

    ax.set_xticks(yearly.index)
    ax.set_xticklabels(['Apr ' + str(year.year) for year in yearly.index])
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(fontsize * .8)

    ax.set_xlabel('Admission date', fontsize=fontsize)
    ax.set_ylabel('Proportion of net costs', fontsize=fontsize)
    ax.legend(fontsize=fontsize * .8)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
