'''
Dag for stocks extract, load and report
'''
from get_companys_overview import get_all_companys_overview
from get_stocks_prices import get_all_stocks_prices
from create_tables import create_tables_from_model
from fetch_stocks_data import generate_weekley_stocks_charts
from fetch_stocks_data import fetch_weekley_stock_data
from fetch_stocks_data import gen_daily_stocks_dataframe
from get_api_data import symbols_list as sl
from database.database import PostgresClient
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

def load_company_overview():
    '''
    Load company overview data
    '''
    symbols_list = sl()
    df_company = get_all_companys_overview(symbols_list)
    postgresclient=PostgresClient()
    postgresclient.insert_from_frame(df_company,'company_overview',if_exists='replace',index=True)

def load_stock_value(**context):
    '''
    Load stock value data
    '''
    date = f"{context['logical_date']:%Y-%m-%d}"
    clean_query= f"DELETE FROM stock_value WHERE date::timestamp::date = '{date}';"
    postgresclient=PostgresClient()
    postgresclient.execute(clean_query)
    df_stocks = get_all_stocks_prices(date,sl())
    if len(df_stocks) > 0:
        print(f'Inserting {len(df_stocks)} rows on stock_value table')
        postgresclient.insert_from_frame(df_stocks,'stock_value',if_exists='append',index=False)
    else:
        print('No data to insert on stock_value table')

def call_generate_weekley_stocks_charts(**context):
    '''
    Call generate_weekley_stocks_charts function
    '''
    date = f"{context['logical_date']:%Y-%m-%d}"
    df_stocks = fetch_weekley_stock_data(date)
    if df_stocks.empty:
        print('No data to generate charts')
        return
    else:
        generate_weekley_stocks_charts(df_stocks,date,'detailed')
        df_daily = gen_daily_stocks_dataframe(df_stocks)
        #
        if len(df_daily['date'].unique()) > 3:
            generate_weekley_stocks_charts(df_daily,date,'daily')
        else:
            print('No enough data to generate daily charts')
            return

default_args = {
    'owner': 'patricio',
    'retries': 0,
    'start_date': datetime(2022, 10, 1),
}
with DAG(
    'stocks_extract_load_report_dag',
    default_args=default_args,
    schedule_interval='5 4 * * TUE-SAT',
    max_active_runs=1
) as dag:
    create_stg1_tables_task = PythonOperator(
        task_id='create_stg1_tables_task',
        python_callable=create_tables_from_model,
        wait_for_downstream=True
    )

    load_company_overview_task = PythonOperator(
        task_id='load_company_overview_task',
        python_callable=load_company_overview
    )

    load_stock_value_task = PythonOperator(
        task_id='load_stock_value_task',
        python_callable=load_stock_value
    )

    generate_weekley_stocks_charts_task = PythonOperator(
        task_id='generate_weekley_stocks_charts_task',
        python_callable=call_generate_weekley_stocks_charts
    )


    final_step = DummyOperator(
        task_id='all_task_completed'
    )

    create_stg1_tables_task>>load_company_overview_task>>load_stock_value_task>>\
    generate_weekley_stocks_charts_task>>final_step
    create_stg1_tables_task>>final_step
