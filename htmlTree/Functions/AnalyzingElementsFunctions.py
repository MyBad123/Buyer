import colorsys
import re

import numpy as np


def convert_color(element):
    l_border = element.color.find("(") + 1
    r_border = element.color.find(")")
    arr = element.color[l_border:r_border].split(",")
    rgba = [float(item) for item in arr]

    if len(rgba) == 4:
        rgba = rgba2rgb(rgba)
    hsv = colorsys.rgb_to_hsv(np.around(rgba[0] / 255, decimals=2), np.around(rgba[1] / 255, decimals=2),
                              np.around(rgba[2] / 255, decimals=2))
    element.hue = np.around(hsv[0], decimals=3)
    element.saturation = np.around(hsv[1], decimals=3)
    element.brightness = np.around(hsv[2], decimals=3)


def rgba2rgb(rgba, background=(255, 255, 255)):
    r, g, b, a = rgba[0], rgba[1], rgba[2], rgba[3]

    R, G, B = background
    rgb = np.zeros(3)
    rgb[0] = round(r * a + (1.0 - a) * R)
    rgb[1] = round(g * a + (1.0 - a) * G)
    rgb[2] = round(b * a + (1.0 - a) * B)

    return rgb


def analyze_text(text, element):
    if re.search('.', text) is not None:
        element.has_point = 1

    digits = re.findall('[0-9]+', text)
    if digits is not None:
        for el in digits:
            element.n_digits += len(el)

    text = text.lower()

    if text.find("₽") != -1 or text.find("руб.") != -1 or text.find("р.") != -1:
        element.presence_of_ruble = 1

    find1 = text.find("артикул")
    find2 = text.find("арт.")
    find3 = text.find("арт:")
    if find1 != -1 or find2 != -1 or find3 != -1:
        element.presence_of_vendor = 1

    if re.search(r'[A-Za-z]', text) is not None and re.search(r'[А-Яа-я]', text) is not None:
        element.writing_form = 3
    if re.search(r'[A-Za-z]', text) is None and re.search(r'[А-Яа-я]', text) is not None:
        element.writing_form = 2
    if re.search(r'[A-Za-z]', text) is not None and re.search(r'[А-Яа-я]', text) is None:
        element.writing_form = 1

    if re.search('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', text) is not None:
        element.presence_of_link = 1

    try:
        number = float(text)
        if number.is_integer():
            element.integer = 1
        else:
            element.float = 1
    except ValueError:
        element.integer = 0

    if text.find("@") != -1:
        element.presence_of_at = 1