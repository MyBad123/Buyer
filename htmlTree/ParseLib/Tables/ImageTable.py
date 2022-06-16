from htmlTree.ParseLib.Tables.TemplateTable import TemplateTable


class ImageTable(TemplateTable):
    def table_name(self):
        return "image" + f"_{self.name}"

    def columns(self):
        return {"id": ["SERIAL", "PRIMARY KEY"],
                "source": ["text"],
                "url": ["text"],
                "width": ["float"],
                "height": ["float"],
                "x": ["float"],
                "y": ["float"],
                "distance_btw_el_and_ruble": ["float"],
                "distance_btw_el_and_article": ["float"]}
