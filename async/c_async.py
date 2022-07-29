import asyncio
import time
from pprint import pprint

import aiohttp


async def call_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    currency = await call_api('http://api.coincap.io/v2/assets')
    currency = [item['id'] for item in currency['data']]
    coros = []
    for item in currency:
        call_api_coro = call_api(f'http://api.coincap.io/v2/assets/{item}')
        coros.append(call_api_coro)
    api_responses = await asyncio.gather(*coros)
    pprint(api_responses)

if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)