from htmlTree.ParseLib.Tables.TemplateTable import TemplateTable


class SiteTable(TemplateTable):
    def table_name(self):
        return "sites"

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"],
                "url": ["text"],
                "emails": ["text"]}
