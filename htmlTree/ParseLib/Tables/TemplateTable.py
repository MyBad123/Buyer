import datetime

import requests

from htmlTree.ParseLib.Postgre.postgre_connection import PostgreConnector


class TemplateTable:
    connection = PostgreConnector()

    def __init__(self):
        self.dbConnection = self.connection
        return

    def table_name(self):
        return self.dbConnection.prefix + "common_table"

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"]}

    def primary_key(self):
        return ['id']

    def column_names(self):
        return self.columns().keys()

    def column_names_without_id(self):
        lst = self.columns()
        if 'id' in lst:
            del lst['id']
        return lst.keys()

    def table_constraints(self):
        return []

    def create(self):
        sql = f"CREATE TABLE IF NOT EXISTS {self.table_name()}("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbConnection.conn.cursor()
        try:
            cur.execute(sql)
            self.dbConnection.conn.commit()
        except:
            requests.get(f"https://buyerdev.1d61.com/set-csv-logs/?error-with-creation-bd")
        return

    def insert_one(self, vals):
        # print(datetime.datetime.now(), ' is ', vals)
        for i in range(0, len(vals)):
            if type(vals[i]) != str:
                vals[i] = str(vals[i])
        sql = f"INSERT INTO {self.table_name()}("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        sql += ", ".join(["%s"]*len(vals)) + ")"
        cur = self.dbConnection.conn.cursor()
        cur.execute(sql, vals)
        self.dbConnection.conn.commit()

        return

    def drop(self):
        sql = f"DROP TABLE IF EXISTS {self.table_name()}"
        cur = self.dbConnection.conn.cursor()
        try:
            cur.execute(sql)
            self.dbConnection.conn.commit()
        except:
            requests.get(f"https://buyerdev.1d61.com/set-csv-logs/?error-with-dropping-bd")
        return

    def all(self):
        sql = f"SELECT * FROM {self.table_name()}"

        cur = self.dbConnection.conn.cursor()
        cur.execute(sql)
        arr = []
        for el in cur.fetchall():
            arr.append(dict(zip(self.column_names(), el)))
        return arr

    def one(self, row_primary_key):
        if not isinstance(row_primary_key, list):
            row_primary_key = [row_primary_key]
        for i in range(0, len(row_primary_key)):
            if type(row_primary_key[i]) != str:
                row_primary_key[i] = str(row_primary_key[i])
        vals = dict(zip(self.primary_key(), row_primary_key))
        arr = [k + " = " + "%s" for k, v in vals.items()]
        sql = f"SELECT * FROM {self.table_name()} WHERE "
        sql += " AND ".join(arr)
        cur = self.dbConnection.conn.cursor()
        cur.execute(sql, list(vals.values()))
        return dict(zip(self.column_names(), cur.fetchone()))

    def count_rows(self):
        sql = f"SELECT COUNT(*) FROM {self.table_name()}"
        cur = self.dbConnection.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()[0]

    def update_row(self, dic_insert, row_primary_key):
        if not isinstance(row_primary_key, list):
            row_primary_key = [row_primary_key]
        for i in range(0, len(row_primary_key)):
            if type(row_primary_key[i]) != str:
                row_primary_key[i] = str(row_primary_key[i])
        primary_key = dict(zip(self.primary_key(), row_primary_key))
        keys = [k + " = " + v for k, v in primary_key.items()]
        sql = f"UPDATE {self.table_name()} SET "
        vals = [k + " = " + "%s" for k, v in dic_insert.items()]
        sql += ", ".join(vals)
        sql += " WHERE "
        sql += " AND ".join(keys)
        cur = self.dbConnection.conn.cursor()
        cur.execute(sql, list(dic_insert.values()))
        self.dbConnection.conn.commit()
