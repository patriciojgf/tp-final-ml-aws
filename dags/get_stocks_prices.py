from time import sleep
import pandas as pd
from get_api_data import call_api

def parse_data(data,symbol) -> pd.DataFrame:
    '''Parse the data and return a dataframe    
    Args:
        data (dict): data from the api call
        symbol (str): stock symbol
    Returns:
        df (pd.DataFrame): dataframe with the data
    '''
    df = pd.DataFrame(data['Time Series (15min)']).T
    df.index.name = 'date'
    df.index = pd.to_datetime(df.index)
    df = df.astype(dtype='float')
    df['symbol_str'] = symbol
    df['created_at_dt'] = pd.to_datetime('now',utc=True)
    df.rename(columns={'1. open':'open_num','2. high':'high_num','3. low':'low_num','4. close':'close_num','5. volume':'volume_num'},inplace=True)
    
    df.reset_index(inplace=True)
    return df

def get_stock_prices(symbol,date) -> pd.DataFrame:
    '''Get stock prices for a symbol
    Args:
        symbol (str): stock symbol
        date (str): date in the format YYYY-MM-DD
    Returns:
        df (pd.DataFrame): dataframe with the stock prices for the date
    '''
    print(f'Getting data for')
    data = call_api(symbol,'TIME_SERIES_INTRADAY')
    df = parse_data(data,symbol)
    df_stock = df[(df['date'].dt.date == pd.to_datetime(date).date())]
    return df_stock

def get_all_stocks_prices(date,list) -> pd.DataFrame:
    '''Get stock prices for all symbols in the list
    
    Args:
        date (str): date in the format YYYY-MM-DD
        list (list): list of stock symbols
    Returns:
        df (pd.DataFrame): dataframe with all the stock prices for the date  
    '''
    df_all = pd.DataFrame()
    for symbol in list:
        df = get_stock_prices(symbol,date)
        #change apend to concat to avoid the error on future versions of pandas
        #df_all = df_all.append(df)
        df_all = pd.concat([df_all,df])        
        sleep(20)
    return df_all
