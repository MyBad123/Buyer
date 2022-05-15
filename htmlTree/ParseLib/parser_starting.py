import uuid
import pathlib
import datetime
from .Functions.Parser import Parser


def start(path, url):
    
    # write logs
    with open(str(pathlib.Path(__file__).parent.parent) + '/pars_log.txt', 'a') as file:
        file.write('\n' + str(datetime.datetime.now()) + ' is start')

    parser = Parser()
    path = parser.site_parsing(url, str(uuid.uuid4()), path)

    return path
