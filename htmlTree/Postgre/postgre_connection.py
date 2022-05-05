import psycopg2
import yaml


class PostgreConnector:
    def __init__(self):
        with open('../config.yaml') as f:
            config = yaml.safe_load(f)
            self.prefix = config['dbtableprefix']
            self.conn = psycopg2.connect(user=config['user'],
                                         password=config['password'],
                                         host=config['host'],
                                         port=config['port'],
                                         database=config['database'])

    def __del__(self):
        if self.conn:
            self.conn.close()
            print("Соединение с PostgreSQL закрыто")
