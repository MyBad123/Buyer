import datetime

import requests

from htmlTree.ParseLib.Postgre.postgre_connection import PostgreConnector


class TemplateTable:
    connection = PostgreConnector()
    log_path = 'log.txt'

    def __init__(self, name=""):
        self.dbConnection = self.connection
        self.name = name
        return

    def change_settings(self):
        sql = 'SET lc_monetary TO "en_US.UTF-8";'
        cur = self.dbConnection.conn.cursor()
        cur.execute(sql)
        self.dbConnection.conn.commit()

    def table_name(self):
        return "elements"

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"],
                "content_element": ["text"],
                "url": ["text"],
                "length": ["integer"],
                "class_ob": ["text"],
                "id_element": ["text"],
                "style": ["text"],
                "enclosure": ["integer"],
                "href": ["text"],
                "count": ["integer"],
                "location_x": ["float"],
                "location_y": ["float"],
                "size_width": ["float"],
                "size_height": ["float"],
                "path": ["text"],
                "integer": ["integer"],
                "float": ["integer"],
                "n_digits": ["integer"],
                "presence_of_ruble": ["integer"],
                "presence_of_vendor": ["integer"],
                "presence_of_link": ["integer"],
                "presence_of_at": ["integer"],
                "has_point": ["integer"],
                "writing_form": ["integer"],
                "font_size": ["text"],
                "font_family": ["text"],
                "color": ["text"],
                "distance_btw_el_and_ruble": ["float"],
                "distance_btw_el_and_article": ["float"],
                "ratio_coordinate_to_height": ["float"],
                "hue": ["float"],
                "saturation": ["float"],
                "brightness": ["float"],
                "background": ["text"],
                "text": ["text"],
                "source": ["text"],
                "site_id": ["integer"]}

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
        except Exception as ex:
            log_file = open(self.log_path, "a+", encoding="UTF-8")
            log_file.write(f"{datetime.datetime.now()} - {ex}\n")
            log_file.close()
            print("error-with-creating-bd")
        return

    def insert_row(self, data, columns):
        cursor = self.dbConnection.conn.cursor()
        for i in range(0, len(data)):
            if type(data[i]) != str:
                data[i] = str(data[i])
        query = "INSERT INTO {} ({})\n".format(self.table_name(), ', '.join(list(columns))) + " VALUES("
        query += ", ".join(["%s"] * len(data)) + ")"
        cursor.execute(query, data)
        self.dbConnection.conn.commit()

        return

    def drop(self):
        sql = f"DROP TABLE IF EXISTS {self.table_name()}"
        cur = self.dbConnection.conn.cursor()
        try:
            cur.execute(sql)
            self.dbConnection.conn.commit()
        except Exception as ex:
            log_file = open(self.log_path, "a+", encoding="UTF-8")
            log_file.write(f"{datetime.datetime.now()} - {ex}\n")
            log_file.close()
            print("error-with-dropping-bd")
        return

    def truncate(self):
        sql = f"TRUNCATE {self.table_name()}"
        cur = self.dbConnection.conn.cursor()
        cur.execute(sql)
        self.dbConnection.conn.commit()

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

    def select(self, param):
        for i, j in param.items():
            if type(j) != str:
                param[i] = str(j)
        arr = [f"{k} = '{v}'" for k, v in param.items()]
        query = f'SELECT * FROM {self.table_name()} WHERE '
        query += " AND ".join(arr + self.table_constraints())
        cur = self.dbConnection.conn.cursor()
        cur.execute(query)
        arr = []
        for el in cur.fetchall():
            arr.append(dict(zip(self.column_names(), el)))
        return arr

    def select_unique(self, columns):
        if not isinstance(columns, list):
            columns = [columns]
        columns = ", ".join(columns)
        sql = f"SELECT DISTINCT {columns} FROM {self.table_name()}"
        cur = self.dbConnection.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

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
