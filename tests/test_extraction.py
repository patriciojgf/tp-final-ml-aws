#One that tests the extraction. This refers to the formatting that takes place after the data is fetched from the API that is to be inserted in the DB.
import sys
import os
PYTHONPATH = os.environ['PYTHONPATH']
sys.path.insert(0, PYTHONPATH + 'dags')
sys.path.insert(0, PYTHONPATH + 'tests')
import pandas as pd
import pytest

from mocks import extract_mock as mock
from get_stocks_prices import parse_data as parse_stocks_prices
from get_companys_overview import parse_data as parse_compay_overview


#generate test that checks that the data is in the correct format
def test_get_all_stocks_prices_format():
    data = mock.call_api('GOOGL','TIME_SERIES_INTRADAY') 
    df = parse_stocks_prices(data,'GOOGL')
    assert df['symbol_str'].dtype == 'object'
    assert df['open_num'].dtype == 'float64'
    assert df['high_num'].dtype == 'float64'
    assert df['low_num'].dtype == 'float64'
    assert df['close_num'].dtype == 'float64'
    assert df['volume_num'].dtype == 'float64'
    assert df['created_at_dt'].dtype == 'datetime64[ns, UTC]'
    assert df['date'].dtype == 'datetime64[ns]'

#generate test that checks that the data is in the correct format
def test_get_all_companys_overview_format():    
    data = mock.call_api('AMZN','OVERVIEW')    
    df = parse_compay_overview(data)
    assert df.index.dtype == 'object'
    assert df['name_str'].dtype == 'object'
    assert df['description_str'].dtype == 'object'
    assert df['exchange_str'].dtype == 'object'
    assert df['created_at_dt'].dtype == 'datetime64[ns, UTC]'

if __name__ == '__main__':
    test_get_all_stocks_prices_format()
    test_get_all_companys_overview_format()