import psycopg2
import yaml
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    with open('../config.yaml') as f:
        config = yaml.safe_load(f)
        connection = psycopg2.connect(user=config['user'],
                                      password=config['password'],
                                      host=config['host'],
                                      port=config['port'])
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        sql_create_database = f"create database {config['database']}"
        cursor.execute(sql_create_database)
except Exception as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
