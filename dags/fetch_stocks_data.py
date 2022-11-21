import plotly.graph_objects as pog
from database.database import PostgresClient
from get_api_data import symbols_list as sl
from datetime import timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt

def fetch_weekley_stock_data(date):
    '''
    Fetches the stock data from the database for the last week
    
    Parameters:
        date (str): date to fetch the data for
    Output:
        df_stocks (pd.DataFrame): dataframe with the stock data    
    '''    
    #cast date to type datetime
    date_d = datetime.strptime(date, '%Y-%m-%d')
    #date minus seven days
    date_w = date_d - timedelta(days=7)
    date_h = date_d + timedelta(days=1)
    postgresclient=PostgresClient()
    query = f"SELECT * FROM stock_value WHERE date BETWEEN '{date_w}' AND '{date_h}';"
    df = postgresclient.to_frame(query)
    return df

def generate_weekley_stocks_charts(df_stocks,date,identificator):
    '''
    Generates the charts for the stocks for the last week
    
    Parameters:
        df_stocks (pd.DataFrame): dataframe with the stock data
        date (str): date to fetch the data for
    Output:
        None
    '''    
    if df_stocks.empty:
        print('No data to generate charts')
        return
    else:        
        df_stocks.index = pd.DatetimeIndex(df_stocks['date'])
        df_stocks.sort_index(inplace=True)
        
        for symbol in sl():
            fig, ax = plt.subplots(figsize=(16, 8))
            df_symbol = df_stocks[df_stocks['symbol_str']==symbol]
            ax.plot(df_symbol['date'],df_symbol['close_num'], label='Close Price for '+symbol)
            ax.plot(df_symbol['date'],df_symbol['high_num'], label='High Price for '+symbol)
            ax.plot(df_symbol['date'],df_symbol['low_num'], label='Low Price for '+symbol)
            ax.plot(df_symbol['date'],df_symbol['open_num'], label='Open Price for '+symbol)
            ax.set_xlabel("Date")
            ax.set_ylabel("Close price")
            ax.set_title("Close price for "+symbol+" from last week")
            ax.legend()
            fig.savefig(f"data/reports/{symbol}_{identificator}_{date}_chart.png")

        
        for symbol in sl():
            print(f"Generating chart for {symbol}")
            print(f"Date: {date}")
            print([df_stocks['symbol_str']])
            df_symbol = df_stocks[df_stocks['symbol_str']==symbol]
            fig = pog.Figure()
            fig.add_trace(pog.Scatter(x=df_symbol['date'], y=df_symbol['close_num'], name="close_num"))
            fig.add_trace(pog.Scatter(x=df_symbol['date'], y=df_symbol['high_num'], name="high_num"))
            fig.add_trace(pog.Scatter(x=df_symbol['date'], y=df_symbol['low_num'], name="low_num"))
            fig.add_trace(pog.Scatter(x=df_symbol['date'], y=df_symbol['open_num'], name="open_num"))
            fig.update_layout(title=f"Stock Price for {symbol}",
                        xaxis_title="Date",
                        yaxis_title="Price",
                        legend_title="Legend Title",
                        font=dict(
                            family="Courier New, monospace",
                            size=18,
                            color="#7f7f7f"
                        ))
            fig.write_html(f"data/reports/{symbol}_{identificator}_{date}.html")
   
   
def gen_daily_stocks_dataframe(dataframe):
    '''
    Filters the dataframe to get one row per day
    Parameters:
        dataframe (pd.DataFrame): dataframe with the stock data
    
    Output:
        df_daily (pd.DataFrame): dataframe with the last register of each day
    '''
    df = dataframe.copy()
    df.index = pd.DatetimeIndex(df['date'])
    df.sort_index(inplace=True)
    df_symbols_list = df['symbol_str'].unique()
    df_daily = pd.DataFrame()
    for symbol in df_symbols_list:
        df_temp = df[df['symbol_str']==symbol].copy()
        df_temp['date'] = df_temp['date'].dt.date
        date_list = df_temp['date'].unique()
        for date in date_list:
            #get lowest num of the day
            low_num = df_temp[df_temp['date']==date]['low_num'].min()
            #get highest num of the day
            high_num = df_temp[df_temp['date']==date]['high_num'].max()
            #get last register of the day and take the close_num
            close_num = df_temp.groupby(pd.Grouper(freq='D')).tail(1)['close_num'].values[0]
            #get first register of the day and take the open_num
            open_num = df_temp.groupby(pd.Grouper(freq='D')).head(1)['open_num'].values[0]
            #get the volume of the day
            volume_num = df_temp[df_temp['date']==date]['volume_num'].sum()
            df_daily = pd.concat([df_daily,pd.DataFrame({'date':[date],
                                                        'symbol_str':[symbol],
                                                        'low_num':[low_num],
                                                        'high_num':[high_num],
                                                        'close_num':[close_num],
                                                        'open_num':[open_num],
                                                        'volume_num':[volume_num]})])
            
    df_daily.reset_index(drop=True, inplace=True)
    return df_daily