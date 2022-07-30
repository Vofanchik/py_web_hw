import asyncio
import time
from pprint import pprint

import aiohttp
from more_itertools import chunked

CONCURENCE = 10

async def call_api(url: str, session:  aiohttp.ClientSession):
    async with session.get(url) as response:
        if response.status == 200:
            response_json = await response.json()
            return response_json
        else:
            pass

async def main():
    async with aiohttp.ClientSession() as session:
        currency = await call_api('http://api.coincap.io/v2/assets', session)
        currency = [item['id'] for item in currency['data']]
        coros = (
            call_api(f'http://api.coincap.io/v2/assets/{coin}', session)
            for coin in currency
        )
        for coros_chunked in chunked(coros, CONCURENCE):
            api_responses = await asyncio.gather(*coros_chunked)
            print(api_responses)

if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)