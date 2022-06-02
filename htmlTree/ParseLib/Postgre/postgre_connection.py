import os

import psycopg2
import yaml

from htmlTree.ParseLib.parser_path import parser_path


class PostgreConnector:
    def __init__(self):
        self.conn = psycopg2.connect(user=os.environ.get('SQL_USER'),
                                     password=os.environ.get('SQL_PASSWORD'),
                                     host=os.environ.get('SQL_HOST'),
                                     port=os.environ.get('SQL_PORT'),
                                     database=os.environ.get('SQL_DATABASE'))

    def __del__(self):
        if self.conn:
            self.conn.close()
            print("Соединение с PostgreSQL закрыто")
