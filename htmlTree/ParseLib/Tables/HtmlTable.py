from htmlTree.ParseLib.Tables.TemplateTable import TemplateTable


class HtmlTable(TemplateTable):
    def table_name(self):
        return "html" + f"_{self.name}"

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"],
                "html": ["text"],
                "url": ["text"],
                "elements": ["text"]}
