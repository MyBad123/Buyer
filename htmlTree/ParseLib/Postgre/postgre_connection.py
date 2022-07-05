import os
import pathlib
from dotenv import load_dotenv

import psycopg2

from htmlTree.ParseLib.parser_path import parser_path


class PostgreConnector:
    def __init__(self):
        # work with env
        path_my_my = str(pathlib.Path(__file__).parent.parent.parent.parent) + '/Buyer/'
        dotenv_path = os.path.join(path_my_my, '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        self.conn = psycopg2.connect(user=os.environ.get('SQL_USER'),
                                     password=os.environ.get('SQL_PASSWORD'),
                                     host=os.environ.get('SQL_HOST'),
                                     port=os.environ.get('SQL_PORT'),
                                     database=os.environ.get('SQL_DATABASE'))

    def __del__(self):
        if self.conn:
            self.conn.close()
            print("Соединение с PostgreSQL закрыто")
