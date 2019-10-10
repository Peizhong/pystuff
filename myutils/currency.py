from collections import namedtuple
import json
import requests

Currency = namedtuple('currency',['code','rate'])

CURRENCY_LINK = 'https://www.mycurrency.net/US.json'
FILE_PATH = 'us.json'

def update_currency():
    print('downloading from: '+CURRENCY_LINK)
    if not True:
        r = requests.get(CURRENCY_LINK, stream=True) # create HTTP response object
        with open(FILE_PATH,'wb') as f:
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    f.write(chunk)
    with open(FILE_PATH,'r') as f:
        cr = json.load(f)
        d = [Currency(c['code'],c['rate']) for c in cr['rates'] ]
        print(d)
        return d

if(__name__ == '__main__'):
    update_currency()