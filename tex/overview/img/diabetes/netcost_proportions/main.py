import os

from matplotlib.dates import date2num
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
import pandas as pd

def plot_netcost_proportions(df):
    """
    A time series plot for the proportion diabetic patients make up of the total
    net cost of a spell by their admission date. See plot_los_time() for details
    on misrepresentation incurred.
    """
    time_constraint = (df['ADMDATE'] >= '2012-04-01') \
                      & (df['DISCDATE'] < '2017-04-30')

    df = df[time_constraint]
    diabetic = df[df['Diabetes'] == 1]

    diabetic_netcost = diabetic.groupby('ADMDATE')['NetCost'].sum()
    total_netcost = df.groupby('ADMDATE')['NetCost'].sum()

    proportions = diabetic_netcost / total_netcost
    proportions.dropna(inplace=True)


    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    monthly = proportions.resample('BM').mean()
    yearly = proportions.resample('BA-APR').mean()
    yearly_err = monthly.resample('BA-APR').std().bfill()

    params = pd.DataFrame(yearly_err).rename({'NetCost': 'err'}, axis=1)
    params['val'] = yearly.values
    params['vmin'] = params['val'] - params['err']
    params['vmax'] = params['val'] + params['err']

    X = date2num(monthly.index.values.reshape(-1, 1))
    y = monthly.values.reshape(-1, 1)

    lr = LinearRegression()
    lr.fit(X, y)
    linreg_df = pd.DataFrame(lr.predict(X), index=monthly.index)

    ax.errorbar(params.index, params['val'], params['err'], capsize=8,
                alpha=0.25, ecolor='k', linestyle='', label='Standard dev.')
    ax.plot(monthly, '.', alpha=0.75, label='End of month avg.')
    ax.plot(yearly, 'x', label='End of year avg.')
    ax.plot(linreg_df, '-', label='Lin. regression model')

    ax.set_xlabel('Admission date')
    ax.set_ylabel('Proportion of total net costs')
    ax.legend(loc='best')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename, transparent=True)
