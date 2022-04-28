import pyodbc
from datetime import datetime

from pandas import read_sql


class Sql:
    def __init__(self, database, server="(local)"):
        self.cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                                   "Server=" + server + ";"
                                                        "Database=" + database + ";"
                                                                                 "Trusted_Connection=yes;")
        self.query = "-- {}\n\n-- Made in Python".format(datetime.now()
                                                         .strftime("%d/%m/%Y"))

    def create_table(self,
                     data=["order", "content_element", "url", "length", "class_ob", "id_element", "style", "enclosure",
                           "href", "text", "count", "location_x", "location_y", "size_width", "size_height", "path",
                           "integer", "float", "n_digits", "presence_of_ruble", "presence_of_vendor",
                           "presence_of_link", "presence_of_at", "has_point", "check_duplicate", "writing_form",
                           "font_size", "font_family", "color", "distance_btw_el_and_ruble",
                           "distance_btw_el_and_article", "ratio_coordinate_to_height", "hue", "saturation",
                           "brightness", "background"], table="Pages"):
        cursor = self.cnxn.cursor()
        cursor.fast_executemany = True

        query = "CREATE TABLE [" + table + "] (\n"

        query += "\t[Id] int PRIMARY KEY IDENTITY(1,1),\n"

        for i in range(len(list(data))):
            query += "\t[{}] varchar(max)".format(list(data)[i])

            if i != len(list(data)) - 1:
                query += ",\n"
            else:
                query += "\n);"

        cursor.execute(query)
        self.cnxn.commit()

        self.query += ("\n\n-- create table\n" + query)

    def insert_row(self, data,
                   df=["order", "content_element", "url", "length", "class_ob", "id_element", "style", "enclosure",
                       "href", "text", "count",
                       "location_x", "location_y", "size_width", "size_height", "path", "integer", "float", "n_digits",
                       "presence_of_ruble", "presence_of_vendor", "presence_of_link", "presence_of_at", "has_point",
                       "writing_form", "font_size", "font_family", "color",
                       "distance_btw_el_and_ruble", "distance_btw_el_and_article", "ratio_coordinate_to_height", "hue",
                       "saturation", "brightness", "background"], table="Pages"):
        cursor = self.cnxn.cursor()
        cursor.fast_executemany = True

        query = ("INSERT INTO [{}] ({})\n".format(table,
                                                  '[' + '], ['
                                                  .join(list(df)) + ']') +
                 "VALUES\n(?{})".format(", ?" * (len(list(df)) - 1)))

        cursor.execute(query, data)
        self.cnxn.commit()

    def manual(self, query, response=False):
        cursor = self.cnxn.cursor()

        if response:
            return read_sql(query, self.cnxn)
        try:
            cursor.execute(query)
        except pyodbc.ProgrammingError as error:
            print("Warning:\n{}".format(error))

        self.cnxn.commit()
        return "Query complete."

    def drop(self, tables="Pages"):
        if isinstance(tables, str):
            tables = [tables]

        for table in tables:
            query = ("IF OBJECT_ID ('[" + table + "]', 'U') IS NOT NULL "
                                                  "DROP TABLE [" + table + "]")
            self.manual(query)

    def select_all(self, tables="Pages"):
        cursor = self.cnxn.cursor()
        return cursor.execute(f"SELECT * FROM {tables}")

    def select_without_duplicates(self, group, table="Pages"):
        cursor = self.cnxn.cursor()
        if isinstance(group, str):
            group = [group]

        group_by = '[' + '], ['.join(group) + ']'
        query = f"""
            SELECT * FROM {table}
            Where [Id]  in
            (
                select min(id) as MinRowID
                FROM {table}
                group by {group_by}
            )
        """
        return cursor.execute(query)

    def delete_template(self, count_of_pages, table='Pages'):
        cursor = self.cnxn.cursor()
        query = f"""
        SELECT DISTINCT text FROM {table}
        """

        for unique_value in cursor.execute(query).fetchall():
            count_value = cursor.execute(f"SELECT COUNT(Id) FROM {table} WHERE text = '{unique_value[0]}'").fetchone()[0]
            query_1 = f"""
                UPDATE {table} SET count = {count_value} WHERE text = '{unique_value[0]}'
            """
            cursor.execute(query_1)

        query = f"""
            DELETE FROM {table} WHERE count > {0.2*count_of_pages} AND n_digits != 11 AND presence_of_at = 0
        """
        cursor.execute(query)
        query = f"""
                    DELETE FROM {table}
                    Where [Id]  not in
                    (
                        select min(id) as MinRowID
                        FROM {table}
                        WHERE n_digits = 11
                    ) AND n_digits = 11
                """
        cursor.execute(query)
        query = f"""
                            DELETE FROM {table}
                            Where [Id]  not in
                            (
                                select min(id) as MinRowID
                                FROM {table}
                                WHERE presence_of_at = 1
                            ) AND presence_of_at = 1
                        """
        cursor.execute(query)
        self.cnxn.commit()
