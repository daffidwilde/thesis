import os

from matplotlib.dates import date2num
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_admissions(df):
    """
    A time series plot for the proportion of daily admissions who are diabetic.
    """
    fontsize = 16

    diabetic = df[df["Diabetes"] == 1]

    admissions = []
    for dataset in (diabetic, df):
        num_admissions = (
            dataset.groupby("ADMDATE")["SPELL_ID"]
            .nunique()
            .reset_index()
            .rename({"SPELL_ID": "n_spells"}, axis=1)
            .groupby("ADMDATE")["n_spells"]
            .sum()
        )

        admissions.append(num_admissions)

    proportions = admissions[0] / admissions[1]
    proportions.dropna(inplace=True)

    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    monthly = proportions.resample("BM").mean()
    yearly = proportions.resample("BA-APR").mean()
    yearly_err = monthly.resample("BA-APR").std().bfill()

    params = pd.DataFrame(yearly_err).rename({"n_spells": "err"}, axis=1)
    params["val"] = yearly.values
    params["vmin"] = params["val"] - params["err"]
    params["vmax"] = params["val"] + params["err"]

    data = monthly
    X, y = (
        date2num(data.index.values.reshape(-1, 1)),
        data.values.reshape(-1, 1),
    )
    lr = LinearRegression()
    lr.fit(X, y)
    y_pred = lr.predict(X)
    linreg_df = pd.DataFrame(y_pred, index=data.index)

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
        ['2012-05-01', 0.0945],
        fontsize=fontsize
    )

    ax.set_xticks(yearly.index)
    ax.set_xticklabels(['Apr ' + str(year.year) for year in yearly.index])
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(fontsize * .8)

    ax.set_xlabel('Admission date', fontsize=fontsize)
    ax.set_ylabel('Proportion of total admissions', fontsize=fontsize)
    ax.legend(fontsize=fontsize * .8)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
