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
        self.background = ""
