from unittest.mock import MagicMock, patch
import pandas as pd
from datetime import datetime, timedelta

#create mock data for call_api function
def fetch_weekley_stock_data(date):
    '''    
    Parameters:
        date (str): date to fetch the data for
    Output:
        df_stocks (pd.DataFrame): dataframe with the stock data    
    '''
    #read json file to dataframe
    df = pd.read_json('tests/raw/2022-10-14_stocks.json')
    return df    

if __name__ == '__main__':
    #create mock data for call_api function
    data = call_api('AMZN','OVERVIEW')