import os

from matplotlib.dates import date2num
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
import pandas as pd

def plot_los_time(df):
    """
    A time series plot showing the average length of stay for diabetic patients
    by their admission date. The purpose of this plot is to observe any patterns
    that are developing over time but it does incur a degree of
    misrepresentation since the individual date of admission is independent
    (largely).
    """
    time_constraint = (df['ADMDATE'] >= '2012-04-01') \
                      & (df['DISCDATE'] < '2017-04-30')

    diabetic = df[(time_constraint) & (df['Diabetes'] == 1)]
    lengths_of_stay = diabetic.set_index('ADMDATE') \
                              .drop_duplicates('SPELL_ID')['TRUE_LOS'] \
                              .dropna()


    fig, ax = plt.subplots(1, figsize=(16, 10), dpi=300)

    monthly = lengths_of_stay.resample('BM').mean()
    monthly = monthly.loc[monthly.index < '2017']
    yearly = lengths_of_stay.resample('BA-APR').mean()
    yearly = yearly.loc[yearly.index < '2017']
    yearly_err = monthly.resample('BA-APR').std().bfill()
    yearly_err = yearly_err.loc[yearly_err.index < '2017']

    params = pd.DataFrame(yearly_err).rename({'TRUE_LOS': 'err'}, axis=1)
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
    ax.set_ylabel('Average length of stay [days]')
    ax.legend(loc='best')

    here = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(here, 'main.pdf')
    plt.savefig(filename)
