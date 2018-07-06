import requests


def getword(word: str):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        r = requests.get('http://www.zdic.net/', headers=header)
        r = requests.post('http://www.zdic.net/sousou/',
                          data=r'lb_a=hp&lb_b=mh&lb_c=mh&tp=tp1&q=%E7%8E%8B', headers=header)

    except Exception as e:
        print(e)
    finally:
        pass


if __name__ == '__main__':
    getword('王')
