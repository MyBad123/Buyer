import uuid
from .Functions.Parser import Parser


def start(path):
    parser = Parser()
    path = parser.site_parsing("https://allflorarium.ru/", str(uuid.uuid4()), path)

    return path