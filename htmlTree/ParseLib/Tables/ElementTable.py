from htmlTree.ParseLib.Tables.TemplateTable import TemplateTable


class ElementTable(TemplateTable):
    def table_name(self):
        return "elements" + f"_{self.name}"
