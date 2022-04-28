import pandas as pd
from htmlTree.Functions import Sql

sql = Sql.Sql('SiteMap')


def create_scv(count_of_page):
    count_of_page = int(count_of_page)
    sql.create_table(table='NewPages')
    for el in sql.select_without_duplicates(group=['url', 'text']).fetchall():
        sql.insert_row(data=[el.order, str(el.content_element), str(el.url), str(el.length), str(el.class_ob),
                             str(el.id_element), str(el.style), str(el.enclosure), str(el.href), str(el.text),
                             str(el.count), str(el.location_x), str(el.location_y), str(el.size_width),
                             str(el.size_height), str(el.path),
                             str(el.integer), str(el.float), str(el.n_digits), str(el.presence_of_ruble),
                             str(el.presence_of_vendor),
                             str(el.presence_of_link), str(el.presence_of_at), str(el.has_point),
                             str(el.writing_form), str(el.font_size), str(el.font_family), str(el.color),
                             str(el.distance_btw_el_and_ruble), str(el.distance_btw_el_and_article),
                             str(el.ratio_coordinate_to_height), str(el.hue), str(el.saturation), str(el.brightness),
                             str(el.background)], table='NewPages')
    sql.drop(tables='Pages')

    sql.delete_template(count_of_page, "NewPages")

    df = pd.DataFrame(data=None,
                      columns=("nn", "class", "text", "presence_of_ruble", "content_element", "url", "length",
                               "class_ob", "element_id", "style", "enclosure", "href", "count", "location_x",
                               "location_y",
                               "size_width", "size_height", "integer", "float", "n_digits", "presence_of_vendor",
                               "presence_of_link", "presence_of_at", "has_point", "writing_form", "font-size", "hue",
                               "saturation", "brightness", "font-family", "ratio_coordinate_to_height",
                               "distance_btw_el_and_ruble", "distance_btw_el_and_article", "id_xpath"))

    for el_to_add in sql.select_all(tables="NewPages"):
        new_row = pd.DataFrame(
            [{"text": el_to_add.text, "presence_of_ruble": el_to_add.presence_of_ruble,
              "content_element": el_to_add.content_element, "url": el_to_add.url, "length": el_to_add.length,
              "class_ob": el_to_add.class_ob, "element_id": el_to_add.id_element, "style": el_to_add.style,
              "enclosure": el_to_add.enclosure, "href": el_to_add.href, "count": el_to_add.count,
              "location_x": el_to_add.location_x, "location_y": el_to_add.location_y,
              "size_width": el_to_add.size_width, "size_height": el_to_add.size_height,
              "integer": el_to_add.integer, "float": el_to_add.float, "n_digits": el_to_add.n_digits,
              "presence_of_vendor": el_to_add.presence_of_vendor, "presence_of_link": el_to_add.presence_of_link,
              "presence_of_at": el_to_add.presence_of_at, "has_point": el_to_add.has_point,
              "writing_form": el_to_add.writing_form, "font-size": el_to_add.font_size, "hue": el_to_add.hue,
              "saturation": el_to_add.saturation, "brightness": el_to_add.brightness,
              "font-family": el_to_add.font_family, "ratio_coordinate_to_height": el_to_add.ratio_coordinate_to_height,
              "distance_btw_el_and_ruble": el_to_add.distance_btw_el_and_ruble,
              "distance_btw_el_and_article": el_to_add.distance_btw_el_and_article,
              "id_xpath": str(el_to_add.content_element) + "//" + str(el_to_add.path) + "//" + str(el_to_add.url)}])
        df = pd.concat([df, new_row])

    df.to_csv('Csv.csv')
    sql.drop(tables='NewPages')
