import uuid
import pathlib
import datetime
from .Functions.Parser import Parser
from multiprocessing import Pool, freeze_support


def start(path, url):
    
    # write logs
    with open(str(pathlib.Path(__file__).parent.parent) + '/pars_log.txt', 'a') as file:
        file.write('\n' + str(datetime.datetime.now()) + ' is start')

    parser = Parser(f'{path}{str(uuid.uuid4())}')
    path = parser.site_parsing(url, str(uuid.uuid4()), path)

    return path


def parallel_start(path, url):
    freeze_support()
    pool = Pool()
    input_path = path.split(",")
    input_url = url.split(",")
    final_values = zip(input_path, input_url)
    result = pool.starmap(start, final_values)

    pool.close()
    pool.join()
