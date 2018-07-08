import asyncio
import aiohttp

import time

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


@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    # Ignore the body, close the socket
    writer.close()


loop = asyncio.get_event_loop()


async def fetch(url):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as html:
            print(html.status)
            response = await html.text(encoding="utf-8")
            # print(response)
            return response

if __name__ == '__main__':
    todo = ['http://www.baidu.com',
            'http://www.ifanr.com', 'http://www.dgtle.com']
    task = [fetch(url) for url in todo]
    loop.run_until_complete(asyncio.gather(*task))
    print('done')
