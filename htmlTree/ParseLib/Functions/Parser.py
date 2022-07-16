import math
import re
import os
import time
from random import random, randint
import difflib as df
import datetime
import pathlib
from dotenv import load_dotenv

import numpy as np
import selenium

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from urllib.parse import urljoin, urlparse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from htmlTree.ParseLib.Functions.CreationCSV import *
from htmlTree.ParseLib.Class.PageElement import Elements
from htmlTree.ParseLib.Tables.ElementTable import *
from htmlTree.ParseLib.Tables.HtmlTable import *
from htmlTree.ParseLib.Tables.ImageTable import *
from htmlTree.ParseLib.Tables.TemplateTable import *
from htmlTree.ParseLib.Tables.SiteTable import *


class MyException(Exception):
    pass


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


class Parser:
    def __init__(self, url, csv_id):
        print(f"Start site parsing with url: {url}")
        self.csv_id = csv_id
        self.ignore = ["#", "tel:"]
        self.list_urls = []
        self.driver = webdriver
        self.count = 0
        self.url = url
        self.domain = re.findall(r'([\w\-:]+)\/\/', url)[0] + '//' + re.findall(r'\/\/([\w\-.]+)', url)[0]
        self.domain_without = max(self.domain.split("//")[-1].split("/")[0].split("."), key=len).replace('-', '_')
        self.domain_name = urlparse(self.url).scheme + "://" + urlparse(self.url).netloc
        self.elementTable = ElementTable(self.domain_without)
        self.htmlTable = HtmlTable(self.domain_without)
        self.imageTable = ImageTable(self.domain_without)
        self.templateTable = TemplateTable()
        self.templateTable.change_settings()
        self.siteTable = SiteTable()
        self.siteTable.create()
        self.templateTable.create()
        self.log_file = None
        self.root_domain = None

    def get_elements(self, site_id):
        try:
            site_html = self.htmlTable.one(site_id)
            list_of_data_xid = list(filter(None, site_html['elements'].split(",")))
            list_of_img_xid = list(filter(None, site_html['images'].split(",")))
            self.driver.get(site_html['url'])
            list_of_elements = []
            beautiful_soup = BeautifulSoup(site_html['html_bs_new'], 'lxml')
            results_of_element = beautiful_soup.findAll()
            for res_of_el in results_of_element:
                if res_of_el.get('data-xid') in list_of_data_xid:
                    par = res_of_el
                    i = 0
                    path_str = ""
                    while par is not None:
                        path_str = str(par.name) + "[" + str(len(par.findAllPrevious())) + "]" + "/" + path_str
                        par = par.parent
                        i += 1

                    if res_of_el.text is not None and len(" ".join(res_of_el.text.split())) > 1:
                        new_el = Elements(res_of_el.name, site_html['url'], len(" ".join(res_of_el.text.split())),
                                          res_of_el.get('class'),
                                          res_of_el.get('id'), " ".join(str(res_of_el.get('style')).split()), i,
                                          res_of_el.get('href'), " ".join(res_of_el.text.split()), path_str)
                        new_el.analyze_text()
                        new_el.order = res_of_el.get('data-xid')
                        list_of_elements.append(new_el)

            new_body = str(beautiful_soup).split("<html>")[-1].split("</html>")[0]
            current_html = self.driver.find_element(by=By.TAG_NAME, value="html")
            self.driver.execute_script("arguments[0].innerHTML = arguments[1]", current_html, new_body)
            driver_elements = self.driver.find_elements(by=By.XPATH, value='//*[@data-xid]')
            img_elements = self.driver.find_elements(by=By.XPATH, value='//*[@img-xid]')
            height = self.driver.execute_script("return document.body.scrollHeight")

            list_of_images = []
            for img in img_elements:
                if img.get_attribute('img-xid') in list_of_img_xid:
                    new_img = Elements("img", site_html['url'], None, None, None, None, None, None, None, None)
                    new_img.source = str(img.get_attribute('src'))
                    new_img.location_x = img.location['x']
                    new_img.location_y = img.location['y']
                    new_img.size_width = str(img.size['width'])
                    new_img.size_height = str(img.size['height'])

                    if new_img.size_height != 0 and new_img.size_width != 0:
                        if re.match(r'^(\/)', new_img.source) is not None:
                            new_img.source = self.domain + new_img.source
                        elif re.match(r'^\.{1,2}', new_img.source) is not None:
                            new_img.source = urljoin(self.domain, new_img.source)
                        list_of_images.append(new_img)

            j = 0
            arr_of_el_with_ruble = []
            arr_of_el_with_article = []
            print(log := f"{site_html['id']}: {site_html['url']} all el: {len(driver_elements)}, " \
                         f"after del: {len(list_of_elements)}")
            self.log_file.write(f"{datetime.datetime.now()} - {log}\n")
            for el in driver_elements:
                if j >= len(list_of_elements):
                    break
                if int(el.get_attribute('data-xid')) == int(list_of_elements[j].order):
                    list_of_elements[j].font_size = el.value_of_css_property('font-size')[:-2]
                    list_of_elements[j].font_family = el.value_of_css_property('font-family')
                    list_of_elements[j].color = el.value_of_css_property('color')
                    list_of_elements[j].color = el.value_of_css_property('background-color')
                    list_of_elements[j].convert_color()

                    list_of_elements[j].location_x = el.location['x']
                    list_of_elements[j].location_y = el.location['y']
                    list_of_elements[j].size_width = el.size['width']
                    list_of_elements[j].size_height = el.size['height']
                    if height != 0:
                        list_of_elements[j].ratio_coordinate_to_height = \
                            np.around(list_of_elements[j].location_y / height, decimals=6)

                    if list_of_elements[j].presence_of_ruble == 1:
                        arr_of_el_with_ruble.append(list_of_elements[j])

                    if list_of_elements[j].presence_of_vendor == 1:
                        arr_of_el_with_article.append(list_of_elements[j])
                    j += 1

            if len(arr_of_el_with_ruble) != 0 or len(arr_of_el_with_article) != 0:
                for el in list_of_elements:
                    if el.location_x != 0:
                        if len(arr_of_el_with_ruble) > 0:
                            delta_x = abs(arr_of_el_with_ruble[0].location_x - el.location_x)
                            delta_y = abs(arr_of_el_with_ruble[0].location_y - el.location_y)
                            el.distance_btw_el_and_ruble = math.sqrt(abs(np.square(delta_x) + np.square(delta_y)))
                            for el_with_ruble in arr_of_el_with_ruble:
                                delta_x = abs(el_with_ruble.location_x - el.location_x)
                                delta_y = abs(el_with_ruble.location_y - el.location_y)
                                distance = math.sqrt(abs(np.square(delta_x) + np.square(delta_y)))
                                if el.distance_btw_el_and_ruble > distance:
                                    el.distance_btw_el_and_ruble = distance

                        if len(arr_of_el_with_article) > 0:
                            delta_x = abs(arr_of_el_with_article[0].location_x - el.location_x)
                            delta_y = abs(arr_of_el_with_article[0].location_y - el.location_y)
                            el.distance_btw_el_and_article = math.sqrt(abs(np.square(delta_x) + np.square(delta_y)))
                            for el_with_article in arr_of_el_with_article:
                                delta_x = abs(el_with_article.location_x - el.location_x)
                                delta_y = abs(el_with_article.location_y - el.location_y)
                                distance = math.sqrt(abs(np.square(delta_x) + np.square(delta_y)))
                                if el.distance_btw_el_and_article > distance:
                                    el.distance_btw_el_and_article = distance

                        el.distance_btw_el_and_article = np.around(el.distance_btw_el_and_article, decimals=3)
                        el.distance_btw_el_and_ruble = np.around(el.distance_btw_el_and_ruble, decimals=3)

                for img in list_of_images:
                    if len(arr_of_el_with_ruble) > 0:
                        delta_x = abs(arr_of_el_with_ruble[0].location_x - img.location_x)
                        delta_y = abs(arr_of_el_with_ruble[0].location_y - img.location_y)
                        img.distance_btw_el_and_ruble = math.sqrt(abs(np.square(delta_x) + np.square(delta_y)))
                        for el_with_ruble in arr_of_el_with_ruble:
                            delta_x = abs(el_with_ruble.location_x - img.location_x)
                            delta_y = abs(el_with_ruble.location_y - img.location_y)
                            distance = math.sqrt(abs(np.square(delta_x) + np.square(delta_y)))
                            if img.distance_btw_el_and_ruble > distance:
                                img.distance_btw_el_and_ruble = distance

                    if len(arr_of_el_with_article) > 0:
                        delta_x = abs(arr_of_el_with_article[0].location_x - img.location_x)
                        delta_y = abs(arr_of_el_with_article[0].location_y - img.location_y)
                        img.distance_btw_el_and_article = math.sqrt(abs(np.square(delta_x) + np.square(delta_y)))
                        for el_with_article in arr_of_el_with_article:
                            delta_x = abs(el_with_article.location_x - img.location_x)
                            delta_y = abs(el_with_article.location_y - img.location_y)
                            distance = math.sqrt(abs(np.square(delta_x) + np.square(delta_y)))
                            if img.distance_btw_el_and_article > distance:
                                img.distance_btw_el_and_article = distance

                    img.distance_btw_el_and_article = np.around(img.distance_btw_el_and_article, decimals=3)
                    img.distance_btw_el_and_ruble = np.around(img.distance_btw_el_and_ruble, decimals=3)
                    self.imageTable.insert_row(data=[img.source, site_html['url'], img.size_width, img.size_height,
                                                     img.location_x, img.location_y,
                                                     str(img.distance_btw_el_and_ruble),
                                                     str(img.distance_btw_el_and_article)],
                                               columns=['source', 'url', 'width', 'height', 'x', 'y',
                                                        'distance_btw_el_and_ruble', 'distance_btw_el_and_article'])

            arr_of_el_with_ruble.clear()
            arr_of_el_with_article.clear()

            for i in range(0, len(list_of_elements)):
                el = list_of_elements[i]
                if el.location_x != 0:
                    self.elementTable.insert_row(
                        data=[str(el.content_element), str(el.url), str(el.length), str(el.class_ob),
                              str(el.id_element), str(el.style), str(el.enclosure), str(el.href),
                              str(el.count), str(el.location_x), str(el.location_y), str(el.size_width),
                              str(el.size_height), str(el.path),
                              str(el.integer), str(el.float), str(el.n_digits), str(el.presence_of_ruble),
                              str(el.presence_of_vendor),
                              str(el.presence_of_link), str(el.presence_of_at), str(el.has_point),
                              str(el.writing_form), str(el.font_size), str(el.font_family), str(el.color),
                              str(el.distance_btw_el_and_ruble), str(el.distance_btw_el_and_article),
                              str(el.ratio_coordinate_to_height), str(el.hue), str(el.saturation),
                              str(el.brightness),
                              str(el.background), el.text.replace("'", "''"), "", 0],
                        columns=self.elementTable.column_names_without_id())

        except selenium.common.exceptions.TimeoutException:
            print(log := f"selenium.common.exceptions.TimeoutException link: {site_html['url']}")
            self.log_file.write(f"{datetime.datetime.now()} - {log}\n")
        except selenium.common.exceptions.WebDriverException as ex:
            print(log := f"selenium.common.exceptions.WebDriverException link: {site_html['url']}, {ex}")
            self.log_file.write(f"{datetime.datetime.now()} - {log}\n")

    def site_parsing(self, uuid4, my_path):
        # work with env
        path_my_my = str(pathlib.Path(__file__).parent.parent.parent.parent) + '/Buyer/'
        dotenv_path = os.path.join(path_my_my, '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        self.root_domain = os.environ.get('ROOT_DOMAIN')
        txt_path = f'{my_path}{uuid4}.txt'
        log_file = open(txt_path, "w+", encoding="UTF-8")
        log_file.close()
        self.log_file = open(txt_path, "a+", encoding="UTF-8")
        self.log_file.write(f"{datetime.datetime.now()} - Start site parsing with url: {self.url}")
        # options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')  # example
        try:
            row = self.siteTable.select(param={"url": self.url})
            csv = Csv(self.domain_without, txt_path, self.csv_id)
            if not row:
                options = Options()
                options.headless = True

                # self.driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.FIREFOX, options=options)
                self.driver = webdriver.Firefox(
                    options=options
                )
                self.driver.maximize_window()

                self.list_urls.append(self.url)
                self.elementTable.create()
                self.htmlTable.create()
                self.imageTable.create()
                self.elementTable.log_path = txt_path
                self.htmlTable.log_path = txt_path
                self.imageTable.log_path = txt_path
                self.templateTable.log_path = txt_path

                self.get_html_site(self.url, 1)
                print(log := f"count of html pages after parsing: {self.htmlTable.count_rows()}")
                self.log_file.write(f"{datetime.datetime.now()} - {log}\n")
                self.delete_pattern()
                self.siteTable.insert_row(data=[str(self.url)], columns=["url"])
                row = self.siteTable.select(param={"url": self.url})
                site_id = row[0]['id']
                path = csv.create_scv(uuid4=uuid4, my_path=my_path, site_id=site_id)
                self.driver.close()
            else:
                site_id = row[0]['id']
                path = csv.create_ex_csv(uuid4=uuid4, my_path=my_path, site_id=site_id)
            self.log_file.close()
            os.remove(txt_path)
            return path
        except Exception as ex:
            self.log_file.write(f"{datetime.datetime.now()} - Exception: {ex}\n")
            self.log_file.close()
            self.elementTable.drop()
            self.imageTable.drop()
            self.htmlTable.drop()
            return txt_path

    def get_html_site(self, link, depth):
        try:
            self.count += 1
            self.driver.get(link)
            order_id = 0
            img_id = 0
            beautiful_soup = BeautifulSoup(self.driver.page_source, 'lxml')
            html_bs = str(beautiful_soup)
            results_of_element = beautiful_soup.findAll()
            for res_of_el in results_of_element:
                if res_of_el is not None and res_of_el.text is not None and res_of_el.name != "script" \
                        and res_of_el.name != "style":
                    if res_of_el.text is not None and len(" ".join(res_of_el.text.split())) > 1:
                        new_element = res_of_el
                        new_element['data-xid'] = order_id
                        res_of_el.replaceWith(new_element)
                        order_id += 1
                    elif res_of_el.name == "img":
                        new_element = res_of_el
                        new_element['img-xid'] = img_id
                        res_of_el.replaceWith(new_element)
                        img_id += 1
            print(log := f"insert into {self.htmlTable.table_name()} with len of pages {len(html_bs.splitlines())}, " \
                         f"{len(str(beautiful_soup).splitlines())} and url = {link}")
            self.log_file.write(f"{datetime.datetime.now()} - {log}\n")
            self.htmlTable.insert_row(data=[html_bs, str(beautiful_soup), link],
                                      columns=['html_bs', 'html_bs_new', 'url'])
            for part_link_page in beautiful_soup.findAll('a'):
                href = str(part_link_page.get('href'))
                if href == "" or href is None:
                    continue
                href = urljoin(self.url, href)
                if not is_valid(href) or href in self.list_urls or self.domain_name not in href or \
                        len(re.findall(r'\.jpg|\.jpeg|\.png|\.pdf|\.mp4|\.JPG|\.PNG|\.PDF$', href)) > 0 or \
                        not any(el not in href for el in self.ignore):
                    continue

                if depth < 7 and self.count < 400:
                    self.list_urls.append(href)
                    rnd = randint(1, 4)
                    time.sleep(1 + rnd)
                    self.get_html_site(href, depth + 1)

        except selenium.common.exceptions.TimeoutException:
            print(log := f"selenium.common.exceptions.TimeoutException: {link}")
            self.log_file.write(f"{datetime.datetime.now()} - {log}\n")
        except selenium.common.exceptions.WebDriverException as ex:
            print(log := f"selenium.common.exceptions.WebDriverException link: {link}, {ex}")
            self.log_file.write(f"{datetime.datetime.now()} - {log}\n")

    def delete_pattern(self):
        arr_html = self.htmlTable.all()
        print(log := f"count of html pages before delete pattern: {len(arr_html)} for site {self.domain}")
        self.log_file.write(f"{datetime.datetime.now()} - {log}\n")
        arr = np.zeros([len(arr_html), len(arr_html)])

        for i in range(len(arr_html)):
            for j in range(len(arr_html)):
                if i != j:
                    str1 = arr_html[i]['html_bs'].splitlines()
                    str2 = arr_html[j]['html_bs'].splitlines()
                    diff = df.unified_diff(str1, str2, lineterm='')
                    count_minus = 0
                    for el in diff:
                        if el[0] == '-':
                            count_minus += 1
                    arr[i][j] = count_minus
                else:
                    arr[i][j] = 10000

        for i in range(len(arr_html)):
            min_val = arr[i][0]
            position = 0
            for j in range(len(arr_html)):
                if arr[i][j] < min_val:
                    min_val = arr[i][j]
                    position = j
            print(log := f"{arr_html[i]['url']} where min = {min_val} and position = {position}")
            self.log_file.write(f"{datetime.datetime.now()} - {log}\n")
            str1 = arr_html[i]['html_bs'].splitlines()
            str2 = arr_html[position]['html_bs'].splitlines()
            str3 = arr_html[i]['html_bs_new'].splitlines()
            diff = df.context_diff(str1, str2, lineterm='')
            unique_str = ""
            for el in diff:
                if el[0] == "!":
                    for k in range(len(str1)):
                        if str1[k] == el[2:]:
                            if re.match(r'^<.+>', str1[k]) is not None:
                                unique_str += str3[k]
                            else:
                                j = k
                                while True:
                                    if len(re.findall(r'<[^/<>]+>', str1[j])) >= \
                                            len(re.findall(r'</[^/<>]+>', str1[j])):
                                        unique_str += str3[j]
                                        if j == 1 or j == 0:
                                            break
                                        unique_str += str3[j-1]
                                        break
                                    if j == 1 or j == 0:
                                        break
                                    unique_str += str3[j]
                                    j -= 1
                            break
            elements = ""
            images = ""
            for reg in re.findall(r'data-xid="\d*"', unique_str):
                elements += re.search(r'\d+', reg)[0] + ","
            for reg in re.findall(r'img-xid="\d*"', unique_str):
                images += re.search(r'\d+', reg)[0] + ","
            self.htmlTable.update_row({"elements": elements}, arr_html[i]['id'])
            self.htmlTable.update_row({"images": images}, arr_html[i]['id'])

        for i in range(len(arr_html)):
            self.get_elements(arr_html[i]['id'])
