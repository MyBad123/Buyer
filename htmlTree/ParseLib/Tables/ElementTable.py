from htmlTree.ParseLib.Tables.TemplateTable import TemplateTable
from htmlTree.ParseLib.Postgre.postgre_connection import PostgreConnector


class ElementTable(TemplateTable):
    connection = PostgreConnector()

    def __init__(self, name):
        self.dbConnection = self.connection
        self.name = name
        return

    def table_name(self):
        return "elements" + f"_{self.name}"

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
