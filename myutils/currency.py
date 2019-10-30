from collections import namedtuple
import json
import requests

Currency = namedtuple('currency',['country','country_zh','sign','rate'])

CURRENCY_LINK = 'https://www.mycurrency.net/US.json'
FILE_PATH = 'private/us.json'

def get_currency():
    print('downloading from: '+CURRENCY_LINK)
    if 1==2:
        r = requests.get(CURRENCY_LINK, stream=True) # create HTTP response object
        with open(FILE_PATH,'wb') as f:
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
    with open(FILE_PATH,'r') as f:
        cr = json.load(f)
        d = [Currency(c['name'],c['name_zh'],c['currency_code'],c['rate']) for c in cr['rates'] ]
        return d

if(__name__ == '__main__'):
    get_currency()