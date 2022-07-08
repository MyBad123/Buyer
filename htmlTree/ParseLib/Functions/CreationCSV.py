import math
import uuid
import pathlib
import datetime
import requests

import pandas as pd
import numpy as np

from htmlTree.ParseLib.parser_path import parser_path
from htmlTree.ParseLib.Tables.ElementTable import *
from htmlTree.ParseLib.Tables.HtmlTable import *
from htmlTree.ParseLib.Tables.ImageTable import *
from htmlTree.ParseLib.Tables.TemplateTable import *
from htmlTree.ParseLib.Tables.SiteTable import *


class Csv:
    def __init__(self, name, log_path, csv_id):
        self.elementTable = ElementTable(name)
        self.htmlTable = HtmlTable(name)
        self.domain_without = name
        self.templateTable = TemplateTable()
        self.siteTable = SiteTable()
        self.imageTable = ImageTable(name)
        self.log_path = log_path
        self.csv_id = csv_id

    def create_scv(self, uuid4, my_path, site_id):
        log_file = open(self.log_path, "a+", encoding="UTF-8")
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv')

        list_of_elements = self.elementTable.all()
        list_of_img = self.imageTable.all()
        print(log := f"Count of elements for site with url: {len(list_of_elements)} and Count of images for site with "
                     f"url: {len(list_of_img)}")
        log_file.write(f"{datetime.datetime.now()} - {log}\n")

        columns = ("nn", "class", "text", "presence_of_ruble", "content_element", "url", "length",
                   "class_ob", "element_id", "style", "enclosure", "href", "count", "location_x",
                   "location_y",
                   "size_width", "size_height", "integer", "float", "n_digits", "presence_of_vendor",
                   "presence_of_link", "presence_of_at", "has_point", "writing_form", "font-size",
                   "hue",
                   "saturation", "brightness", "font-family", "ratio_coordinate_to_height",
                   "distance_btw_el_and_ruble", "distance_btw_el_and_article", "id_xpath")

        filter_img = pd.DataFrame(data=None, columns=["url", "size", "ruble", "article"])
        urls = self.imageTable.select_unique("url")
        for url in urls:
            new_row = pd.DataFrame([{"url": url[0], "size": 0, "ruble": 0, "article": 0}])
            filter_img = pd.concat([filter_img, new_row])
        for img in list_of_img:
            size = math.sqrt(np.square(float(img["width"])) + np.square(float(img["height"])))
            if size > list(filter_img.loc[filter_img["url"] == img["url"], "size"])[0]:
                filter_img.loc[filter_img["url"] == img["url"], "size"] = size
            if img['distance_btw_el_and_ruble'] > list(filter_img.loc[filter_img["url"] == img["url"], "ruble"])[0]:
                filter_img.loc[filter_img["url"] == img["url"], "ruble"] = img['distance_btw_el_and_ruble']
            if img['distance_btw_el_and_article'] > list(filter_img.loc[filter_img["url"] == img["url"], "article"])[0]:
                filter_img.loc[filter_img["url"] == img["url"], "article"] = img['distance_btw_el_and_article']

        img_dict = {}
        arr_dict = {}
        for img in list_of_img:
            size = math.sqrt(np.square(float(img["width"])) + np.square(float(img["height"])))
            max_size = list(filter_img.loc[filter_img["url"] == img["url"], "size"])[0]
            max_ruble = list(filter_img.loc[filter_img["url"] == img["url"], "ruble"])[0]
            if max_ruble == 0:
                max_ruble = 1
            max_article = list(filter_img.loc[filter_img["url"] == img["url"], "article"])[0]
            if max_article == 0:
                max_article = 1
            indicator = 0.3 * size / max_size + 0.3 * (1 - img['distance_btw_el_and_ruble'] / max_ruble) \
                        + 0.3 * (1 - img['distance_btw_el_and_article'] / max_article)
            if indicator > arr_dict.get(img["url"], 0):
                arr_dict[img["url"]] = indicator
                img_dict[img["url"]] = img

        dup_list = pd.DataFrame(data=None, columns=["check_dup"])
        new_list = []
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-2')
        print(log := "Start delete duplicate")
        log_file.write(f"{datetime.datetime.now()} - {log}\n")
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

        print(log := f"Count of elements after removal duplicate for site with url: {len(new_list)}")
        log_file.write(f"{datetime.datetime.now()} - {log}\n")

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-3')
        list_of_elements.clear()
        df = pd.DataFrame(data=None, columns=columns)

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-4')
        border = self.htmlTable.count_rows() * 0.9
        emails = []
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
                row = {"text": el_to_add['text'], "presence_of_ruble": el_to_add['presence_of_ruble'],
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
                       "distance_btw_el_and_article": el_to_add['distance_btw_el_and_article']}
                if el_to_add['presence_of_at'] == 1 and el_to_add['length'] < 30:
                    emails.append(el_to_add['text'])
                self.templateTable.insert_row(data=[*row.values(), site_id], columns=[*row.keys(), "site_id"])
                row["id_xpath"] = str(el_to_add['content_element']) + "//" + str(el_to_add['path']) + "//" + \
                                  str(el_to_add['url'])
                new_row = pd.DataFrame([row])
                df = pd.concat([df, new_row])
        emails = ", ".join(emails)
        self.siteTable.update_row(dic_insert={"emails": emails}, row_primary_key=site_id)
        for img in img_dict.values():
            row = {'source': img['source'], 'url': img['url'], 'size_width': img["width"],
                   'size_height': img["height"], 'location_x': img["x"], 'location_y': img["y"],
                   'distance_btw_el_and_ruble': img["distance_btw_el_and_ruble"],
                   'distance_btw_el_and_article': img["distance_btw_el_and_article"], "content_element": "img",
                   "text": None, "presence_of_ruble": 0, "length": 0, "class_ob": None, "id_element": None,
                   "style": None, "enclosure": 0, "href": None, "count": 0, "integer": 0, "float": 0, "n_digits": 0,
                   "presence_of_vendor": 0, "presence_of_link": 0, "presence_of_at": 0, "has_point": 0,
                   "writing_form": 0, "font_size": None, "hue": 0, "saturation": 0, "brightness": 0,
                   "font_family": None, "ratio_coordinate_to_height": 0}
            self.templateTable.insert_row(data=[*row.values(), site_id], columns=[*row.keys(), "site_id"])
            new_row = pd.DataFrame([row])
            df = pd.concat([df, new_row])
        path = f'{my_path}{uuid4}.csv'
        print(log := f"Count of elements after removal along the border for site with url: {df.shape[0]}")
        log_file.write(f"{datetime.datetime.now()} - {log}\n")
        log_file.close()
        df.to_csv(path)

        if self.csv_id is not None:
            print(log := f"Work with textBlockClassifier")
            log_file.write(f"{datetime.datetime.now()} - {log}\n")
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = f'path=https://buyerdev.1d61.com/get-csv-file/?id={self.csv_id}'
            try:
                r = requests.post('http://localhost:8000', headers=headers, data=data)
                el_class = r.json()['classes']
                dictionary_class = {
                    0: "не определено",
                    1: "название",
                    2: "цена",
                    3: "описание",
                    4: "артикул",
                    5: "телефон",
                    6: "e-mail"
                }
                el_class = list(map(lambda cl: dictionary_class[int(cl)], el_class))
                print(log := f"Count of classes = {len(el_class)} and count of rows = {df.shape}")
                log_file.write(f"{datetime.datetime.now()} - {log}\n")
                df["class"] = el_class
            except Exception as ex:
                print(log := f"exception with request: {ex}")
                self.log_file.write(f"{datetime.datetime.now()} - {log}\n")

        df.to_csv(path)
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-5')
        self.elementTable.drop()
        self.htmlTable.drop()
        self.imageTable.drop()

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=create-csv-end')
        return path

    def create_ex_csv(self, uuid4, my_path, site_id):
        log_file = open(self.log_path, "a+", encoding="UTF-8")
        df = pd.DataFrame(data=None, columns=["nn", "class"])
        for elDic in self.templateTable.select(param={"site_id": site_id}):
            new_row = pd.DataFrame(
                [{"text": elDic['text'], "presence_of_ruble": elDic['presence_of_ruble'],
                  "content_element": elDic['content_element'], "url": elDic['url'],
                  "length": elDic['length'],
                  "class_ob": elDic['class_ob'], "id_element": elDic['id_element'],
                  "style": elDic['style'],
                  "enclosure": elDic['enclosure'], "href": elDic['href'], "count": elDic['count'],
                  "location_x": elDic['location_x'], "location_y": elDic['location_y'],
                  "size_width": elDic['size_width'], "size_height": elDic['size_height'],
                  "integer": elDic['integer'], "float": elDic['float'], "n_digits": elDic['n_digits'],
                  "presence_of_vendor": elDic['presence_of_vendor'],
                  "presence_of_link": elDic['presence_of_link'],
                  "presence_of_at": elDic['presence_of_at'], "has_point": elDic['has_point'],
                  "writing_form": elDic['writing_form'], "font_size": elDic['font_size'],
                  "hue": elDic['hue'],
                  "saturation": elDic['saturation'], "brightness": elDic['brightness'],
                  "font_family": elDic['font_family'],
                  "ratio_coordinate_to_height": elDic['ratio_coordinate_to_height'],
                  "distance_btw_el_and_ruble": elDic['distance_btw_el_and_ruble'],
                  "distance_btw_el_and_article": elDic['distance_btw_el_and_article'],
                  "id_xpath": str(elDic['content_element']) + "//" + str(elDic['path']) + "//" + str(elDic['url']),
                  "source": elDic["source"]}])
            df = pd.concat([df, new_row])
        path = f'{my_path}{uuid4}.csv'
        df.to_csv(path)
        if self.csv_id is not None:
            print(log := f"Work with textBlockClassifier")
            log_file.write(f"{datetime.datetime.now()} - {log}\n")
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = f'path=https://buyerdev.1d61.com/get-csv-file/?id={self.csv_id}'
            try:
                r = requests.post('http://localhost:8000', headers=headers, data=data)
                el_class = r.json()['classes']
                dictionary_class = {
                    0: "не определено",
                    1: "название",
                    2: "цена",
                    3: "описание",
                    4: "артикул",
                    5: "телефон",
                    6: "e-mail"
                }
                el_class = list(map(lambda cl: dictionary_class[int(cl)], el_class))
                print(log := f"Count of classes = {len(el_class)} and count of rows = {df.shape}")
                log_file.write(f"{datetime.datetime.now()} - {log}\n")
                df["class"] = el_class
            except Exception as ex:
                print(log := f"exception with request: {ex}")
                self.log_file.write(f"{datetime.datetime.now()} - {log}\n")

        df.to_csv(path)
        return path
