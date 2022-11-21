import pandas as pd
import requests
import os
import numpy as np

def get_api_key() -> str:
    '''Get the api key
    Returns:
        api_key (str): api key
    '''
    api_key_list = os.environ.get('ALPHA_VANTAGE_API_KEY').split(',')
    api_key = np.random.choice(api_key_list,1)[0]
    print(f'Your API key is: {api_key}')    
    return api_key
        
def symbols_list() -> list:
    '''Get a list of symbols
    Returns:
        symbol_list (list): list of symbols
    '''
    symbol_list = []
    with open('data/stocks_list.txt', 'r') as f:
        for line in f:
            symbol_list.append(line.strip())         
    return symbol_list
        
def call_api(symbol,function) -> pd.DataFrame:
    '''Call alphavantage api and return the data
    Args:
        symbol (str): stock symbol
        function (str): function to call
        
    Returns:
        data (dict): data from the api call
    '''
    api_key=get_api_key()
    url= f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval=15min&outputsize=full&apikey={api_key}'
    print(url)
    r = requests.get(url)
    data = r.json()
    #
    return data

if __name__ == '__main__':
    get_api_key()