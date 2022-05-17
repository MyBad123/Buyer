import uuid
import pathlib
import requests
import datetime
from .Functions.Parser import Parser


def start(path, url):
    
    # write logs
    requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=start')

    parser = Parser()
    path = parser.site_parsing(url, str(uuid.uuid4()), path)

    return path
