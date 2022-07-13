from parsel import Selector
import requests
from urllib.parse import urljoin, unquote

def bytes_to_date(d):
    d = int(d)
    year = '20{:02d}'.format(d>>9)
    month = '{:02d}'.format((d>>5)&15)
    day = '{:02d}'.format(d&31)
    return f'{year}-{month}-{day}'

def fix_inn(inn):
    inn = str(inn)
    if len(inn) in {9, 11}:
        return '0'+inn
    return inn


def get_file_links(uri):
        egrul = requests.get(uri)
        sel = Selector(egrul.text)

        return [
            urljoin(uri, unquote(link))
            for link in sel.css("a::attr(href)").extract()
            if link.endswith("zip") or link.endswith("csv")
        ]
