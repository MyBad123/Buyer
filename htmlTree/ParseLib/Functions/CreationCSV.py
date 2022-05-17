import uuid
import pathlib
import datetime

import pandas as pd

from htmlTree.ParseLib.parser_path import parser_path
from htmlTree.ParseLib.Tables.ElementTable import *
from htmlTree.ParseLib.Tables.HtmlTable import *


class Csv:
    elementTable = ElementTable()
    htmlTable = HtmlTable()

    def create_scv(self, uuid4, my_path):
        # write logs
        with open(str(pathlib.Path(__file__).parent.parent.parent) + '/pars_log.txt', 'a') as file:
            file.write('\n' + str(datetime.datetime.now()) + ' is start')

        list_of_elements = self.elementTable.all()
        columns = ("nn", "class", "text", "presence_of_ruble", "content_element", "url", "length",
                   "class_ob", "element_id", "style", "enclosure", "href", "count", "location_x",
                   "location_y",
                   "size_width", "size_height", "integer", "float", "n_digits", "presence_of_vendor",
                   "presence_of_link", "presence_of_at", "has_point", "writing_form", "font-size",
                   "hue",
                   "saturation", "brightness", "font-family", "ratio_coordinate_to_height",
                   "distance_btw_el_and_ruble", "distance_btw_el_and_article", "id_xpath")
        self.elementTable.drop()
        new_list = pd.DataFrame(data=None, columns=[*columns, "check_dup"])

        for el in list_of_elements:
            check_dup = el['text'] + el['url']
            if check_dup not in new_list['check_dup'].unique():
                max_en = 0
                for sub_el in list_of_elements:
                    if sub_el['url'] == el['url'] and sub_el['text'] == el['text'] and max_en < int(sub_el['enclosure']):
                        max_en = int(el['enclosure'])

                indicator = True
                for sub_el in list_of_elements:
                    if sub_el['enclosure'] == max_en and sub_el['url'] == el['url'] \
                            and sub_el['text'] == el['text']:
                        if indicator:
                            new_row = pd.DataFrame(
                                [{"text": sub_el['text'], "presence_of_ruble": sub_el['presence_of_ruble'],
                                  "content_element": sub_el['content_element'], "url": sub_el['url'],
                                  "length": sub_el['length'], "check_dup": check_dup,
                                  "class_ob": sub_el['class_ob'], "id_element": sub_el['id_element'],
                                  "style": sub_el['style'],
                                  "enclosure": sub_el['enclosure'], "href": sub_el['href'],
                                  "count": sub_el['count'],
                                  "location_x": sub_el['location_x'], "location_y": sub_el['location_y'],
                                  "size_width": sub_el['size_width'], "size_height": sub_el['size_height'],
                                  "integer": sub_el['integer'], "float": sub_el['float'],
                                  "n_digits": sub_el['n_digits'], "presence_of_vendor": sub_el['presence_of_vendor'],
                                  "presence_of_link": sub_el['presence_of_link'],
                                  "presence_of_at": sub_el['presence_of_at'], "has_point": sub_el['has_point'],
                                  "writing_form": sub_el['writing_form'], "font_size": sub_el['font_size'],
                                  "hue": sub_el['hue'],
                                  "saturation": sub_el['saturation'], "brightness": sub_el['brightness'],
                                  "font_family": sub_el['font_family'],
                                  "ratio_coordinate_to_height": sub_el['ratio_coordinate_to_height'],
                                  "distance_btw_el_and_ruble": sub_el['distance_btw_el_and_ruble'],
                                  "distance_btw_el_and_article": sub_el['distance_btw_el_and_article'],
                                  "id_xpath": str(sub_el['content_element']) + "//" + str(sub_el['path']) + "//" + str(sub_el['url'])}])
                            new_list = pd.concat([new_list, new_row])
                            indicator = False

        list_of_elements.clear()
        df = pd.DataFrame(data=None, columns=columns)

        border = self.htmlTable.count_rows() * 0.5
        for ind1, el_to_add in new_list.iterrows():
            count = 0
            for ind2, sub_el in new_list.iterrows():
                if sub_el['text'] == el_to_add['text']:
                    count += 1
            el_to_add['count'] = count
            need_to_add = False
            if el_to_add['text'] not in df['text'].unique() and \
                    (el_to_add['n_digits'] == 11 or el_to_add['presence_of_at'] == 1) and el_to_add['count'] > border:
                need_to_add = True
            elif el_to_add['count'] < border:
                need_to_add = True

            if need_to_add:
                new_row = pd.DataFrame(
                    [{"text": el_to_add['text'], "presence_of_ruble": el_to_add['presence_of_ruble'],
                      "content_element": el_to_add['content_element'], "url": el_to_add['url'],
                      "length": el_to_add['length'],
                      "class_ob": el_to_add['class_ob'], "id_element": el_to_add['id_element'],
                      "style": el_to_add['style'],
                      "enclosure": el_to_add['enclosure'], "href": el_to_add['href'], "count": el_to_add['count'],
                      "location_x": el_to_add['location_x'], "location_y": el_to_add['location_y'],
                      "size_width": el_to_add['size_width'], "size_height": el_to_add['size_height'],
                      "integer": el_to_add['integer'], "float": el_to_add['float'], "n_digits": el_to_add['n_digits'],
                      "presence_of_vendor": el_to_add['presence_of_vendor'],
                      "presence_of_link": el_to_add['presence_of_link'],
                      "presence_of_at": el_to_add['presence_of_at'], "has_point": el_to_add['has_point'],
                      "writing_form": el_to_add['writing_form'], "font_size": el_to_add['font_size'],
                      "hue": el_to_add['hue'],
                      "saturation": el_to_add['saturation'], "brightness": el_to_add['brightness'],
                      "font_family": el_to_add['font_family'],
                      "ratio_coordinate_to_height": el_to_add['ratio_coordinate_to_height'],
                      "distance_btw_el_and_ruble": el_to_add['distance_btw_el_and_ruble'],
                      "distance_btw_el_and_article": el_to_add['distance_btw_el_and_article'],
                      "id_xpath": el_to_add['id_xpath']}])
                df = pd.concat([df, new_row])
        path = f'{my_path}{uuid4}.csv'
        df.to_csv(path)

        self.elementTable.drop()
        self.htmlTable.drop()

        return path
