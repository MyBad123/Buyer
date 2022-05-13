import requests
from bs4 import BeautifulSoup
import random
import re


def find_results(text):
    url = 'https://google.com/search?q=' + text
    A = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
         )

    Agent = A[random.randrange(len(A))]

    headers = {'user-agent': Agent}
    r = requests.get(url, headers=headers)
    list_of_links = []
    soup = BeautifulSoup(r.text, 'lxml')
    for link in soup.find_all('a'):
        has_h3 = False
        for child in link.findChildren():
            if child.name == 'h3':
                has_h3 = True
        if has_h3:
            list_of_links.append(re.findall(r'url=.*&ved', link.get('href'))[0][4:-4])

    return list_of_links
