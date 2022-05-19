import math
import requests
import re
import os
import time
from random import random, randint
import difflib as df
import datetime
import pathlib
from turtle import st
from dotenv import load_dotenv

import numpy as np
import selenium

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from htmlTree.ParseLib.Functions.CreationCSV import *
from htmlTree.ParseLib.Class.PageElement import Elements
from htmlTree.ParseLib.Tables.ElementTable import *
from htmlTree.ParseLib.Tables.HtmlTable import *


class MyException(Exception):
    pass


class Parser:
    ignore = ["#"]
    domain = ''
    list_urls = []
    order_id = 0
    driver = webdriver
    elementTable = ElementTable()
    htmlTable = HtmlTable()
    count = 0

    def get_elements(self, site_id):
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-elements')
        try:
            site_html = self.htmlTable.one(site_id)
            list_of_data_xid = list(filter(None, site_html['elements'].split(",")))
            self.driver.get(site_html['url'])
            list_of_elements = []
            beautiful_soup = BeautifulSoup(site_html['html'], 'lxml')
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
                        new_el = Elements(0, res_of_el.name, site_html['url'], len(" ".join(res_of_el.text.split())),
                                          res_of_el.get('class'),
                                          res_of_el.get('id'), " ".join(str(res_of_el.get('style')).split()), i,
                                          res_of_el.get('href'), " ".join(res_of_el.text.split()), path_str)
                        new_el.analyze_text()
                        list_of_elements.append(new_el)

            new_body = str(beautiful_soup).split("<html>")[-1].split("</html>")[0]
            current_html = self.driver.find_element(by=By.TAG_NAME, value="html")
            self.driver.execute_script("arguments[0].innerHTML = arguments[1]", current_html, new_body)
            driver_elements = self.driver.find_elements(by=By.XPATH, value='//*[@data-xid]')
            height = self.driver.execute_script("return document.body.scrollHeight")
            j = 0
            arr_of_el_with_ruble = []
            arr_of_el_with_article = []
            for i in range(0, len(list_of_elements)):
                if int(driver_elements[j].get_attribute('data-xid')) == i and j < len(driver_elements) - 1:
                    list_of_elements[i].font_size = driver_elements[j].value_of_css_property('font-size')[:-2]
                    list_of_elements[i].font_family = driver_elements[j].value_of_css_property('font-family')
                    list_of_elements[i].color = driver_elements[j].value_of_css_property('color')
                    list_of_elements[i].color = driver_elements[j].value_of_css_property('background-color')
                    list_of_elements[i].convert_color()

                    list_of_elements[i].location_x = driver_elements[j].location['x']
                    list_of_elements[i].location_y = driver_elements[j].location['y']
                    list_of_elements[i].size_width = driver_elements[j].size['width']
                    list_of_elements[i].size_height = driver_elements[j].size['height']
                    if height != 0:
                        list_of_elements[i].ratio_coordinate_to_height = \
                            np.around(list_of_elements[i].location_y / height, decimals=6)
                    j += 1

                if list_of_elements[i].presence_of_ruble == 1:
                    arr_of_el_with_ruble.append(list_of_elements[i])

                if list_of_elements[i].presence_of_vendor == 1:
                    arr_of_el_with_article.append(list_of_elements[i])

            if len(arr_of_el_with_ruble) != 0 or len(arr_of_el_with_article) != 0:
                for i in range(0, len(list_of_elements)):
                    if list_of_elements[i].location_x != 0:
                        if len(arr_of_el_with_ruble) > 0:
                            delta_x = abs(arr_of_el_with_ruble[0].location_x - list_of_elements[i].location_x)
                            delta_y = abs(arr_of_el_with_ruble[0].location_y - list_of_elements[i].location_y)
                            list_of_elements[i].distance_btw_el_and_ruble = \
                                math.sqrt(delta_x * delta_x + delta_y * delta_y)
                            for el_with_ruble in arr_of_el_with_ruble:
                                delta_x = abs(el_with_ruble.location_x - list_of_elements[i].location_x)
                                delta_y = abs(el_with_ruble.location_y - list_of_elements[i].location_y)
                                if list_of_elements[i].distance_btw_el_and_ruble > \
                                        math.sqrt(delta_x * delta_x + delta_y * delta_y):
                                    list_of_elements[i].distance_btw_el_and_ruble = \
                                        math.sqrt(delta_x * delta_x + delta_y * delta_y)

                        if len(arr_of_el_with_article) > 0:
                            delta_x = abs(arr_of_el_with_article[0].location_x - list_of_elements[i].location_x)
                            delta_y = abs(arr_of_el_with_article[0].location_y - list_of_elements[i].location_y)
                            list_of_elements[i].distance_btw_el_and_article = \
                                math.sqrt(delta_x * delta_x + delta_y * delta_y)
                            for el_with_article in arr_of_el_with_article:
                                delta_x = abs(el_with_article.location_x - list_of_elements[i].location_x)
                                delta_y = abs(el_with_article.location_y - list_of_elements[i].location_y)
                                if list_of_elements[i].distance_btw_el_and_article > \
                                        math.sqrt(delta_x * delta_x + delta_y * delta_y):
                                    list_of_elements[i].distance_btw_el_and_article = \
                                        math.sqrt(delta_x * delta_x + delta_y * delta_y)

                        list_of_elements[i].distance_btw_el_and_article = \
                            np.around(list_of_elements[i].distance_btw_el_and_article, decimals=3)
                        list_of_elements[i].distance_btw_el_and_ruble = \
                            np.around(list_of_elements[i].distance_btw_el_and_ruble, decimals=3)
            arr_of_el_with_ruble.clear()
            arr_of_el_with_article.clear()

            for i in range(0, len(list_of_elements)):
                el = list_of_elements[i]
                if el.location_x != 0:
                    self.elementTable.insert_one(
                        vals=[el.order, str(el.content_element), str(el.url), str(el.length), str(el.class_ob),
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
                              str(el.background), el.text.replace("'", "''")])

        except selenium.common.exceptions.TimeoutException:
            print("selenium.common.exceptions.TimeoutException")
        except selenium.common.exceptions.WebDriverException:
            print("selenium.common.exceptions.WebDriverException")

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-elements-end')

    def site_parsing(self, url, uuid4, my_path):

        # work with env
        path_my_my = str(pathlib.Path(__file__).parent.parent.parent.parent) + '/Buyer/'
        dotenv_path = os.path.join(path_my_my, '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)


        # options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')  # example

        options = Options()
        options.headless = True

        # self.driver = webdriver.Remote("http://selenium:4444/wd/hub", DesiredCapabilities.FIREFOX, options=options)
        self.driver = webdriver.Firefox(
           firefox_profile=os.environ.get('WEBDRIVER_PATH', '/opt/homebrew/Cellar/geckodriver/0.31.0/bin'),
           options=options
        )
        self.driver.maximize_window()

        self.list_urls.append(url)
        self.domain = re.findall(r'([\w\-:]+)\/\/', url)[0] + '//' + re.findall(r'\/\/([\w\-.]+)', url)[0]
        self.elementTable.create()
        self.htmlTable.create()

        # write logs
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=site-parsing-start')

        self.get_html_site(url, 1)
        self.delete_pattern()

        csv = Csv()
        path = csv.create_scv(uuid4, my_path)
        self.driver.close()

        return path

    def get_html_site(self, link, depth):
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-html-site')
        try:
            if depth < 3 and self.count < 1000:
                self.count += 1
                self.driver.get(link)
                order_id = 0
                beautiful_soup = BeautifulSoup(self.driver.page_source, 'lxml')
                results_of_element = beautiful_soup.findAll()
                for res_of_el in results_of_element:
                    if res_of_el is not None and res_of_el.text is not None and res_of_el.name != "script" \
                            and res_of_el.name != "style":
                        if res_of_el.text is not None and len(" ".join(res_of_el.text.split())) > 1:
                            new_element = res_of_el
                            new_element['data-xid'] = order_id
                            res_of_el.replaceWith(new_element)
                            order_id += 1

                new_body = str(beautiful_soup).split("<html>")[-1].split("</html>")[0]
                current_html = self.driver.find_element(by=By.TAG_NAME, value="html")
                self.driver.execute_script("arguments[0].innerHTML = arguments[1]", current_html, new_body)
                self.htmlTable.insert_one(vals=[self.driver.page_source, link, ''])

                for part_link_page in beautiful_soup.findAll('a'):
                    if self.domain in str(part_link_page.get('href')):
                        link_page = str(part_link_page.get('href'))
                    elif re.match(r'^(\/)\w+', str(part_link_page.get('href'))) is not None:
                        link_page = self.domain + str(part_link_page.get('href'))
                    else:
                        continue

                    if link_page not in self.list_urls and str(part_link_page.get('href'))[1] not in self.ignore \
                            and len(re.findall(r'\.jpg|\.jpeg|\.png|\.pdf|\.mp4|\.JPG|\.PNG|\.PDF$',
                                               str(part_link_page.get('href')))) < 1:
                        self.list_urls.append(link_page)
                        rnd = randint(1, 4)
                        time.sleep(1 + rnd)
                        self.get_html_site(link_page, depth + 1)

            requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-html-site-end')

        except selenium.common.exceptions.TimeoutException:
            print("selenium.common.exceptions.TimeoutException: " + link)
        except selenium.common.exceptions.WebDriverException:
            print("selenium.common.exceptions.WebDriverException: " + link)

    def delete_pattern(self):
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=delete-pattern')
        arr_html = self.htmlTable.all()
        arr = np.zeros([len(arr_html), len(arr_html)])

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=delete-pattern-before-1-for')
        for i in range(len(arr_html)):
            for j in range(i, len(arr_html)):
                if i != j:
                    str1 = arr_html[i]['html'].splitlines()
                    str2 = arr_html[j]['html'].splitlines()
                    diff = df.unified_diff(str1, str2, lineterm='')
                    count_plus = 0
                    count_minus = 0
                    for el in diff:
                        if el[0] == '+':
                            count_plus += 1
                        if el[0] == '-':
                            count_minus += 1
                    arr[i][j] = count_minus
                    arr[j][i] = count_plus
                else:
                    arr[i][j] = 5000

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=delete-pattern-before-2-for')
        for i in range(len(arr_html)):
            min_val = arr[0][i]
            position = 0
            for j in range(len(arr_html)):
                if arr[j][i] < min_val:
                    min_val = arr[j][i]
                    position = j
            str1 = arr_html[i]['html'].splitlines()
            str2 = arr_html[position]['html'].splitlines()
            diff = df.unified_diff(str1, str2, lineterm='')
            unique_str = ''
            for el in diff:
                if el[0] == '-':
                    unique_str += el
            elements = ""
            for reg in re.findall(r'data-xid="\d*"', unique_str):
                elements += re.search(r'\d+', reg)[0] + ","
            self.htmlTable.update_row({"elements": f'{elements}'}, arr_html[i]['id'])

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=delete-pattern-before-3-for')
        for i in range(len(arr_html)):
            self.get_elements(arr_html[i]['id'])

        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=delete-pattern-end')
