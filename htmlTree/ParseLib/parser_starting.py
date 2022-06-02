import uuid
import os
import pathlib
import requests
import datetime
from dotenv import load_dotenv
from .Functions.Parser import Parser
from multiprocessing import Pool, freeze_support


def start(path, url):
    # work with env
    path_my_my = str(pathlib.Path(__file__).parent.parent.parent.parent) + '/Buyer/'
    dotenv_path = os.path.join(path_my_my, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    print("???????????????")
    print(os.environ.get('DATABASES'))
    print(os.environ.get('WEBDRIVER_PATH'))
    print("???????????????")
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
