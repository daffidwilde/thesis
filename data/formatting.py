""" All the formatting functions. """

import pandas as pd

def add_HRG_Subchapter(df):
    """ Adds  an HRG Subchapter column to the dataframe. """

    # Subchapter is given by the irst and second letter of HRG

    if 'HRG_Subchapter' not in df.columns:
        df['HRG_Subchapter'] = df['HRG'].map(lambda x: str(x)[:2])

def remove_extra_columns(df):
    """ Removes extra columns added after collection: PODHRG, LogLOS,
    LogNetCost, binary columns for age and days of the week. """

    daysoftheweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                     'Saturday', 'Sunday']
    procedure_on = [f'Procedure on {day}' for day in daysoftheweek]

    cols = ['PODHRG', 'LogLOS', 'LogNetCost', 'LOAD_DATE'] \
           + daysoftheweek + procedure_on \
           + ['Age 1-18', 'Age 19-25', 'Age 26-35', 'Age 36-45',
              'Age 46-55', 'Age 56-75', 'Age 76-90', 'Age >90']

    for col in cols:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)

def format_period(string):
    """ Add a hyphen between the fourth and fifth elements of a string. """
    return string[:4] + '-' + string[4:]

def format_period_cols(df):
    """ Reformats the PERIOD/BENCH_PERIOD columns from 201310 to 2013-10. """

    for col in ['PERIOD', 'BENCH_PERIOD']:
        if col in df.columns:
            df[col].map(format_period)

def format_dates(df):
    """ Reformats the EPISODE_START, EPISODE_END, ADMDATE, DISCDATE, LOAD_DATE,
    procedure_date_dt. """

    cols = ['EPISODE_START', 'EPISODE_END', 'ADMDATE', 'DISCDATE',
            'procedure_date_dt']

    for col in cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

def rename_columns(df):
    """ Rename some of the poorly/confusingly named columns. """

    rename_cols = {'VisonSec': 'VisionSec', 'HIVPrim.1': 'HIV_Prim',
                   'HIVSec.1': 'HIV_Sec', 'LDPrim.1': 'LD_Prim',
                   'LDSec.1': 'LD_Sec', 'site1': 'site', 'C.DIFF': 'C_DIFF'}

    for col, val in rename_cols.items():
        if col in df.columns:
            df.rename(index=str, columns={col: val})
