import colorsys
import re

import numpy as np


def rgba2rgb(rgba, background=(255, 255, 255)):
    r, g, b, a = rgba[0], rgba[1], rgba[2], rgba[3]

    R, G, B = background
    rgb = np.zeros(3)
    rgb[0] = round(r * a + (1.0 - a) * R)
    rgb[1] = round(g * a + (1.0 - a) * G)
    rgb[2] = round(b * a + (1.0 - a) * B)

    return rgb


class Elements:
    def __init__(self, order, content_element, url, length, class_ob, element_id, style, enclosure, href, text, path):
        self.order = order
        self.content_element = content_element
        self.url = url
        self.length = length
        if class_ob is None:
            self.class_ob = 'None'
        else:
            self.class_ob = class_ob
        if element_id is None:
            self.id_element = 'None'
        else:
            self.id_element = element_id
        self.style = style
        self.enclosure = enclosure
        if href is None:
            self.href = 'None'
        else:
            self.href = href
        self.text = text
        self.count = 0
        self.location_x = 0
        self.location_y = 0
        self.size_width = 0
        self.size_height = 0
        self.path = path
        self.integer = 0
        self.float = 0
        self.n_digits = 0
        self.presence_of_ruble = 0
        self.presence_of_vendor = 0
        self.presence_of_link = 0
        self.presence_of_at = 0
        self.has_point = 0
        self.writing_form = 0
        self.font_size = ""
        self.font_family = ""
        self.color = ""
        self.distance_btw_el_and_ruble = 0
        self.distance_btw_el_and_article = 0
        self.ratio_coordinate_to_height = 0
        self.hue = 0
        self.saturation = 0
        self.brightness = 0
        self.background = None

    def convert_color(self):
        l_border = self.color.find("(") + 1
        r_border = self.color.find(")")
        arr = self.color[l_border:r_border].split(",")
        rgba = [float(item) for item in arr]

        if len(rgba) == 4:
            rgba = rgba2rgb(rgba)
        hsv = colorsys.rgb_to_hsv(np.around(rgba[0] / 255, decimals=2), np.around(rgba[1] / 255, decimals=2),
                                  np.around(rgba[2] / 255, decimals=2))
        self.hue = np.around(hsv[0], decimals=3)
        self.saturation = np.around(hsv[1], decimals=3)
        self.brightness = np.around(hsv[2], decimals=3)

    def analyze_text(self):
        if re.search('.', self.text) is not None:
            self.has_point = 1

        digits = re.findall('[0-9]+', self.text)
        if digits is not None:
            for el in digits:
                self.n_digits += len(el)

        text = self.text.lower()

        if text.find("₽") != -1 or text.find("руб.") != -1 or len(re.findall(r' р.', text)) > 0 \
                or len(re.findall(r' руб$', text)) > 0 or len(re.findall(r' руб ', text)) > 0 \
                or len(re.findall(r'\dруб', text)) > 0 or len(re.findall(r'\dр', text)) > 0:
            self.presence_of_ruble = 1

        find1 = text.find("артикул")
        find2 = text.find("арт.")
        find3 = text.find("арт:")
        if find1 != -1 or find2 != -1 or find3 != -1:
            self.presence_of_vendor = 1

        if re.search(r'[A-Za-z]', text) is not None and re.search(r'[А-Яа-я]', text) is not None:
            self.writing_form = 3
        if re.search(r'[A-Za-z]', text) is None and re.search(r'[А-Яа-я]', text) is not None:
            self.writing_form = 2
        if re.search(r'[A-Za-z]', text) is not None and re.search(r'[А-Яа-я]', text) is None:
            self.writing_form = 1

        if re.search('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text) is not None:
            self.presence_of_link = 1

        try:
            number = float(text)
            if number.is_integer():
                self.integer = 1
            else:
                self.float = 1
        except ValueError:
            self.integer = 0

        if text.find("@") != -1:
            self.presence_of_at = 1
