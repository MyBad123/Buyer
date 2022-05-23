from htmlTree.ParseLib.Tables.TemplateTable import TemplateTable
from htmlTree.ParseLib.Postgre.postgre_connection import PostgreConnector


class HtmlTable(TemplateTable):
    connection = PostgreConnector()

    def __init__(self, name):
        self.dbConnection = self.connection
        self.name = name
        return

    def table_name(self):
        return "html" + f"_{self.name}"

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"],
                "html": ["text"],
                "url": ["text"],
                "elements": ["text"]}
