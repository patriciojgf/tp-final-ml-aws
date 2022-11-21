from time import sleep
import pandas as pd
from get_api_data import call_api

def parse_data(data) -> pd.DataFrame:
    '''Parse the data and return a dataframe    
    Args:
        data (dict): data from the api call
        symbol (str): stock symbol
    Returns:
        df (pd.DataFrame): dataframe with the data
    '''
    df = pd.DataFrame(data,index=['0'])[['Symbol','AssetType','Name','Currency','Description','Exchange','Country','Sector','Industry']]
    df.rename(columns={'Symbol':'symbol_str','AssetType':'asset_type_str','Name':'name_str','Currency':'currency_str','Description':'description_str','Exchange':'exchange_str','Country':'country_str','Sector':'sector_str','Industry':'industry_str'},inplace=True)
    
    df = df.set_index('symbol_str')
    df['created_at_dt'] = pd.to_datetime('now',utc=True)
    return df

def get_company_overview(symbol) -> pd.DataFrame:
    '''Get company overview for a symbol
    Args:
        symbol (str): stock symbol
        date (str): date in the format YYYY-MM-DD
    Returns:
        df (pd.DataFrame): dataframe with company overview
    '''
    data = call_api(symbol,'OVERVIEW')
    df = parse_data(data)
    #breakpoint()
    return df

def get_all_companys_overview(list) -> pd.DataFrame:
    '''Get company overview for all symbols in the list
    Args:
        list (list): list of stock symbols
    Returns:
        df (pd.DataFrame): dataframe with all the company overview  
    '''
    df_all = pd.DataFrame()
    for symbol in list:
        df = get_company_overview(symbol)
        #change apend to concat to avoid the error on future versions of pandas
        #df_all = df_all.append(df)
        df_all = pd.concat([df_all,df])    
        sleep(20)    
    return df_all
