import sys
import os
import pandas as pd
import pytest

PYTHONPATH = os.environ['PYTHONPATH']
sys.path.insert(0, PYTHONPATH + 'dags')
sys.path.insert(0, PYTHONPATH + 'tests')
from mocks import db_mock as mock

from fetch_stocks_data import gen_daily_stocks_dataframe


def test_gen_daily_stocks_dataframe_types():
    '''
    test that the data is in the correct format
    '''
    df_stocks=mock.fetch_weekley_stock_data('2022-10-14')
    df_daily = gen_daily_stocks_dataframe(df_stocks)
    assert df_daily['symbol_str'].dtype == 'object'
    assert df_daily['open_num'].dtype == 'float64'
    assert df_daily['high_num'].dtype == 'float64'
    assert df_daily['low_num'].dtype == 'float64'
    assert df_daily['close_num'].dtype == 'float64'

def test_only_one_row_per_date():
    '''
    test that there is only one row per date
    '''
    df_stocks=mock.fetch_weekley_stock_data('2022-10-14')
    df_daily = gen_daily_stocks_dataframe(df_stocks)
    
    df_symbols_list = df_daily['symbol_str'].unique()
    for symbol in df_symbols_list:
        date_list = df_daily['date'].unique()
        for date in date_list:
            df_daily_filtered = df_daily[(df_daily['symbol_str']==symbol) & (df_daily['date']==date)]
            assert len(df_daily_filtered) == 1
    
    
if __name__ == '__main__':
    test_gen_daily_stocks_dataframe_types()
    test_only_one_row_per_date()