import datetime
from htmlTree.ParseLib.Postgre.postgre_connection import PostgreConnector


class ElementTable:
    connection = PostgreConnector()

    def __init__(self):
        self.dbConnection = self.connection
        return

    def table_name(self):
        return self.dbConnection.prefix + "elements"

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"],
                "el_order": ["integer"],
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
                "text": ["text"]}

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
        cur.execute(sql)
        self.dbConnection.conn.commit()
        return

    def insert_one(self, vals):
        print(datetime.datetime.now(), ' is ', vals)
        for i in range(0, len(vals)):
            if type(vals[i]) != str:
                vals[i] = str(vals[i])
        sql = f"INSERT INTO {self.table_name()}("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        sql += ", ".join(["%s"]*len(vals)) + ")"
        cur = self.dbConnection.conn.cursor()
        try:
            cur.execute(sql, vals)
            self.dbConnection.conn.commit()
        except:
            pass
        return

    def drop(self):
        sql = f"DROP TABLE IF EXISTS {self.table_name()}"
        cur = self.dbConnection.conn.cursor()
        cur.execute(sql)
        self.dbConnection.conn.commit()
        return

    def all(self):
        sql = f"SELECT * FROM {self.table_name()}"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())

        # my | create new connection
        self.dbConnection = PostgreConnector()

        cur = self.dbConnection.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def delete_template(self, count_of_pages, table='Pages'):
        cursor = self.cnxn.cursor()
        query = f"""
        SELECT DISTINCT text FROM {table}
        """

        for unique_value in cursor.execute(query).fetchall():
            count_value = \
                cursor.execute(f"SELECT COUNT(Id) FROM {table} WHERE text = '{unique_value[0]}'").fetchone()[0]
            query_1 = f"""
                UPDATE {table} SET count = {count_value} WHERE text = '{unique_value[0]}'
            """
            cursor.execute(query_1)
        count_of_pages = int(count_of_pages * 0.2)
        query = f"""
            DELETE FROM {table} WHERE count > {count_of_pages} AND n_digits != 11 AND presence_of_at = 0
        """

        cursor.execute(query)
        query = f"""
                    DELETE FROM {table}
                    Where [Id]  not in
                    (
                        select min(id) as MinRowID
                        FROM {table}
                        WHERE n_digits = 11
                    ) AND n_digits = 11 AND count > {count_of_pages}
                """
        cursor.execute(query)
        query = f"""
                            DELETE FROM {table}
                            Where [Id]  not in
                            (
                                select min(id) as MinRowID
                                FROM {table}
                                WHERE presence_of_at = 1
                            ) AND presence_of_at = 1 AND count > {count_of_pages}
                        """
        cursor.execute(query)
        self.cnxn.commit()
