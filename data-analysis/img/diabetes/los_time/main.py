import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import date2num
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


def plot_los_time(df):
    """
    A time series plot showing the average length of stay for diabetic patients
    by their admission date. The purpose of this plot is to observe any patterns
    that are developing over time but it does incur a degree of
    misrepresentation since the individual date of admission is independent
    (largely).
    """
    fontsize = 16

    diabetic = df[df["Diabetes"] == 1]
    lengths_of_stay = (
        diabetic.set_index("ADMDATE").drop_duplicates("SPELL_ID")["TRUE_LOS"].dropna()
    )

    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    monthly = lengths_of_stay.resample("BM").mean()
    monthly = monthly.loc[monthly.index < "2017"]
    yearly = lengths_of_stay.resample("BA-APR").mean()
    yearly = yearly.loc[yearly.index < "2017"]
    yearly_err = monthly.resample("BA-APR").std().bfill()
    yearly_err = yearly_err.loc[yearly_err.index < "2017"]

    params = pd.DataFrame(yearly_err).rename({"TRUE_LOS": "err"}, axis=1)
    params["val"] = yearly.values
    params["vmin"] = params["val"] - params["err"]
    params["vmax"] = params["val"] + params["err"]

    X, y = (
        date2num(monthly.index.values.reshape(-1, 1)),
        monthly.values.reshape(-1, 1),
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
        r"$R^2 = $ " + str(r_squared) + "\n" + r"$SE = $ " + str(standard_err),
        ["2016-09-01", 7.4],
        fontsize=fontsize,
    )

    ax.set_xticks(yearly.index)
    ax.set_xticklabels(["Apr " + str(year.year) for year in yearly.index])
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(fontsize * 0.8)

    ax.set_xlabel("Admission date", fontsize=fontsize)
    ax.set_ylabel("Length of stay (days)", fontsize=fontsize)
    ax.legend(fontsize=fontsize * 0.8)

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, "main.pdf")
    plt.tight_layout()
    plt.savefig(filename, transparent=True)
