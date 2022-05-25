import uuid
import pathlib
import requests
import datetime
from .Functions.Parser import Parser
from multiprocessing import Pool, freeze_support


def start(path, url):
    parser = Parser(url)
    path = parser.site_parsing(str(uuid.uuid4()), path)

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
