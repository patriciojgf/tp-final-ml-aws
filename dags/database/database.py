from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import os

POSTGRESQL_DB_USER = os.environ.get('POSTGRES_DB_USER')
POSTGRESQL_DB_PASSWORD = os.environ.get('POSTGRES_DB_PASSWORD')
POSTGRESQL_HOSTNAME = os.environ.get('POSTGRES_DB_HOST')

Base = declarative_base()

class DB_API:
    def __init__(self, db):
        pass
    
    def _get_engine(self):
        pass
    
    def _connect(self):
        pass
    
    @staticmethod
    def _cursor_columns(cursor):
        pass
    
    def execute(self, query, connection=None):
        pass
    
    def insert_from_frame(self, df, table, if_exists='append', index=False, **kwargs):
        pass
    
    def to_frame(self, *args, **kwargs):
        pass
    

class PostgresClient(DB_API):
    def __init__(self):
        self.dialect = 'postgresql'
        #self.db = db
        self._engine = None
    
    def _get_engine(self):
        print('Creating engine')
        conn_string =  f"postgresql://{POSTGRESQL_DB_USER}:{POSTGRESQL_DB_PASSWORD}@{POSTGRESQL_HOSTNAME}:5432/{POSTGRESQL_DB_USER}"
        print(conn_string)
        if not self._engine:
            self._engine = create_engine(conn_string)
        return self._engine
    
    def _connect(self):
        print('Connecting to database')
        return self._get_engine().connect()
    
    @staticmethod
    def _cursor_columns(cursor):
        print('Getting columns')
        if hasattr(cursor,'keys'):
            return cursor.keys()
        else:
            return [c[0] for c in cursor.description]
    
    def execute(self, query, connection=None):
        print('Executing query')
        if connection is None:
            connection = self._connect()
        return connection.execute(query)
    
    def insert_from_frame(self, df, table, if_exists='append', index=False, **kwargs):
        connection = self._connect()
        with connection:
            df.to_sql(table, connection, if_exists=if_exists, index=index, **kwargs)
    
    def to_frame(self, *args, **kwargs):
        cursor = self.execute(*args, **kwargs)
        if not cursor:
            return None
        data = cursor.fetchall()
        if data:
            df = pd.DataFrame(data, columns=self._cursor_columns(cursor))
        else:
            df = pd.DataFrame()
        return df
