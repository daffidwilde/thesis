import pandas as pd
import numpy as np
import sys

csv_path = str(sys.argv[1])

df = pd.read_csv(csv_path, dtype={'INTERNAL_ID': str, 'SPECIALTY': str, 'BENCH_PERIOD': str, 'PERIOD': str, 'SEX': str}, low_memory=False)

### Formatting ###


def add_HRG_columns(df):
    
    """ Adds an HRG Chapter column and an HRG Subchapter column to 
        the dataframe just before the HRG column.
    """
    
    # Subchapter is given by the irst and second letter of HRG

    if 'HRG_Subchapter' not in df.columns:
        df['HRG_Subchapter'] = df['HRG'].map(lambda x: str(x)[:2])


def remove_extra_columns(df):
    
    """ Removes extra columns added after collection: PODHRG, LogLOS, 
        LogNetCost, binary columns for age and DotW.
    """

    daysoftheweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                     'Friday', 'Saturday', 'Sunday']
    procedure_on = [f'Procedure on {day}' for day in daysoftheweek]
    
    extra_columns = ['PODHRG', 'LogLOS', 'LogNetCost'] + daysoftheweek + procedure_on + ['Age 1-18', 'Age 19-25', 'Age 26-35', 'Age 36-45', 'Age 46-55', 'Age 56-75', 'Age 76-90', 'Age >90']
    
    for col in extra_columns:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)


def format_periods(df):
    
    """ Reformats the PERIOD/BENCH_PERIOD columns from 201310 
        to 2013-10 (for example)
    """

    # Place a hyphen after the fourth character

    if 'Period' not in df.columns:
        period = [df['PERIOD'][i][:4] + '-' + df['PERIOD'][i][4:] for i in range(len(df['PERIOD']))]
        df.insert(loc=df.columns.get_loc('PERIOD'), column='Period', value=period)
        df.drop('PERIOD', axis=1, inplace=True)
    if 'Bench_Period' not in df.columns:
        bench_period = [df['BENCH_PERIOD'][i][:4] + '-' + df['BENCH_PERIOD'][i][4:] for i in range(len(df['BENCH_PERIOD']))]
        df.insert(loc=df.columns.get_loc('BENCH_PERIOD'), column='Bench_Period', value=bench_period)
        df.drop('BENCH_PERIOD', axis=1, inplace=True)


def format_dates(df):

    """ Reformats the EPISODE_START, EPISODE_END, ADMDATE, DISCDATE, 
        LOAD_DATE, procedure_date_dt
    """
    
    date_columns = ['EPISODE_START', 'EPISODE_END', 'ADMDATE', 
                    'DISCDATE', 'LOAD_DATE', 'procedure_date_dt']

    for col in date_columns:
        if col in df.columns:
            df[col] = df[col].map(lambda x: pd.to_datetime(x))


def format_sex(df):
    
    """ Reformats SEX column from 1 or 2 to M or F, respectively, and NaN otherwise.
    """
 
    df.loc[df.SEX == '1', 'SEX'] = 'M'
    df.loc[df.SEX == '2', 'SEX'] = 'F'
    df.loc[(df.SEX != '1') & (df.SEX != '2') & (df.SEX != 'M') & (df.SEX != 'F'), 'SEX'] = np.nan


add_HRG_columns(df)
remove_extra_columns(df)
format_periods(df)
format_sex(df)

df.to_csv(csv_path[:21] + csv_path[33:], header=True, index=False)
