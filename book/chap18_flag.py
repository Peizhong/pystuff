import asyncio


@asyncio.coroutine
def get_flag(cc):
    d = yield from range(10)
    r = yield from range(10)


@asyncio.coroutine
def download_one(cc):
    image = yield from get_flag(cc)
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_do = [download_one(cc) for cc in sorted(cc_list)]
    wait_coro = asyncio.wait(to_do)
    res, _ loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)
