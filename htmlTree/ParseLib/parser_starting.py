import uuid
from .Functions.Parser import Parser


def start(path, url):
    parser = Parser()
    path = parser.site_parsing(url, str(uuid.uuid4()), path)

    return path
