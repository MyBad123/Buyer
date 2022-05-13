import math
import re
import time
from random import random, randint

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


class Parser:
    ignore = ["#"]
    domain = ''
    list_urls = []
    order_id = 0
    count_of_page = 0
    driver = webdriver
    elementTable = ElementTable()

    def find_links(self, link, depth):
        try:
            if depth < 2:
                self.driver.get(link)
                list_of_elements = []
                self.count_of_page += 1
                order_id = 0
                beautiful_soup = BeautifulSoup(self.driver.page_source, 'lxml')
                results_of_element = beautiful_soup.findAll()
                for res_of_el in results_of_element:
                    if res_of_el is not None and res_of_el.text is not None and res_of_el.name != "script" \
                            and res_of_el.name != "style":
                        par = res_of_el
                        i = 0
                        path_str = ""
                        while par is not None:
                            par['dara-order'] = order_id - 1
                            path_str = str(par.name) + "[" + str(len(par.findAllPrevious())) + "]" + "/" + path_str
                            par = par.parent
                            i += 1

                        if res_of_el.text is not None and len(" ".join(res_of_el.text.split())) > 1:
                            new_element = res_of_el
                            new_element['data-xid'] = order_id
                            res_of_el.replaceWith(new_element)

                            new_el = Elements(order_id, res_of_el.name, link, len(" ".join(res_of_el.text.split())),
                                              res_of_el.get('class'),
                                              res_of_el.get('id'), " ".join(str(res_of_el.get('style')).split()), i,
                                              res_of_el.get('href'), " ".join(res_of_el.text.split()), path_str)
                            new_el.analyze_text()
                            list_of_elements.append(new_el)
                            order_id += 1

                new_body = str(beautiful_soup).split("<html>")[-1].split("</html>")[0]
                current_html = self.driver.find_element(by=By.TAG_NAME, value="html")
                self.driver.execute_script("arguments[0].innerHTML = arguments[1]", current_html, new_body)
                driver_elements = self.driver.find_elements(by=By.XPATH, value='//*[@data-xid]')
                height = self.driver.execute_script("return document.body.scrollHeight")
                j = 0
                arr_of_el_with_ruble = []
                arr_of_el_with_article = []
                for i in range(0, order_id):
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
                    for i in range(0, order_id):
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

                for i in range(0, order_id):
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
                        self.find_links(link_page, depth + 1)
        except selenium.common.exceptions.TimeoutException:
            print("selenium.common.exceptions.TimeoutException: " + link)
        except selenium.common.exceptions.WebDriverException:
            print("selenium.common.exceptions.WebDriverException: " + link)

    def site_parsing(self, url, uuid4, my_path):
        print(my_path)
        options = Options()
        options.headless = True
'''
        self.driver = webdriver.Firefox(
            firefox_profile='/opt/homebrew/Cellar/geckodriver/0.31.0/bin',
            options=options
        )
'''

        self.driver = webdriver.Remote(
            f"http://selenium:4444/wd/hub",
            options=options, 
            DesiredCapabilities.CHROME
        )
        
        self.driver.maximize_window()

        self.list_urls.append(url)
        self.domain = re.findall(r'([\w\-:]+)\/\/', url)[0] + '//' + re.findall(r'\/\/([\w\-.]+)', url)[0]
        self.elementTable.create()

        self.find_links(url, 1)
        csv = Csv()
        path = csv.create_scv(self.count_of_page, uuid4, my_path)
        self.driver.close()

        return path
