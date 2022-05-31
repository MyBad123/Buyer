import uuid
import pathlib
import datetime
import requests

import pandas as pd

from htmlTree.ParseLib.parser_path import parser_path
from htmlTree.ParseLib.Tables.ElementTable import *
from htmlTree.ParseLib.Tables.HtmlTable import *


class Csv:
    def __init__(self, name):
        self.elementTable = ElementTable(name)
        self.htmlTable = HtmlTable(name)

    def create_scv(self, uuid4, my_path):
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv')

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
        dup_list = pd.DataFrame(data=None, columns=["check_dup"])
        new_list = []
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-2')
        for el in list_of_elements:
            check_dup = el['text'] + el['url']
            if check_dup not in dup_list['check_dup'].unique():
                max_en = 0
                max_en_el = ''
                for sub_el in list_of_elements:
                    if sub_el['url'] == el['url'] and sub_el['text'] == el['text'] and max_en < int(
                            sub_el['enclosure']):
                        max_en = int(el['enclosure'])
                        max_en_el = sub_el
                new_list.append(max_en_el)
                new_row = pd.DataFrame([{"check_dup": check_dup}])
                dup_list = pd.concat([dup_list, new_row], ignore_index=True)
        list_of_elements.clear()

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-3')
        list_of_elements.clear()
        df = pd.DataFrame(data=None, columns=columns)

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-4')
        border = self.htmlTable.count_rows() * 0.9
        for el_to_add in new_list:
            if int(el_to_add['count']) == 0:
                count = 0
                ind_of_copies = []
                for i in range(len(new_list)):
                    if new_list[i]['text'] == el_to_add['text']:
                        count += 1
                        ind_of_copies.append(i)
                for i in ind_of_copies:
                    new_list[i]['count'] = count
            need_to_add = False
            if el_to_add['text'] not in df['text'].unique() and \
                    (el_to_add['n_digits'] == 11 or el_to_add['presence_of_at'] == 1) \
                    and int(el_to_add['count']) > border:
                need_to_add = True
            elif int(el_to_add['count']) < border:
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

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-5')
        self.elementTable.drop()
        self.htmlTable.drop()

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-end')
        return path
