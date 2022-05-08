import os

from django.db import connection

cursor = connection.cursor()
cursor.execute(
    '''
    SELECT datname FROM pg_catalog.pg_database WHERE datname='parser_db'
    '''
)
result = cursor.fetchone()
if not result:
    cursor.execute(
        '''
        CREATE DATABASE parser_db;
        '''
    )
    cursor.fetchone()


parser_path = os.path.join(os.path.dirname(__file__))